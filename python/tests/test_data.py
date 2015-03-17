import sys, os.path, random, math
import pytest

import support

support.setup_paths()

from pykalibera.data import Data, _confidence_slice_indicies, _mean
from pykalibera.data import confidence_slice, _geomean

# ----------------------------------
# HELPER FIXTURES
# ----------------------------------

@pytest.fixture
def rdata():
    """ Returns some random data """
    return random.sample(xrange(1000), 1000)

# ----------------------------------
# TESTS BEGIN
# ----------------------------------

def test_indicies():
    d = Data({
        (0, 0) : [1, 2, 3, 4, 5],
        (0, 1) : [3, 4, 5, 6, 7]
        }, [1, 2, 5])

    assert d[0, 0, 0] == 1
    assert d[0, 0, 4] == 5
    assert d[0, 1, 2] == 5

def test_rep_levels():
    d = Data({
        (0, 0) : [1, 2, 3, 4, 5],
        (0, 1) : [3, 4, 5, 6, 7]
        }, [1, 2, 5])

    assert d.r(1) == 5 # lowest level, i.e. arity of the lists in the map
    assert d.r(2) == 2
    assert d.r(3) == 1

    # indexs are one based, so 0 or less is invalid
    with pytest.raises(AssertionError):
        d.r(0)
    with pytest.raises(AssertionError):
        d.r(-1337)

    # Since we have 3 levels here, levels 4 and above are bogus
    with pytest.raises(AssertionError):
        d.r(4)
    with pytest.raises(AssertionError):
        d.r(666)

def test_index_iter():
    d = Data({
        (0, 0) : [1, 2, 3, 4, 5],
        (0, 1) : [3, 4, 5, 6, 7]
        }, [1, 2, 5])

    assert list(d.index_iterator()) == [
            (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4),
            (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3), (0, 1, 4),
            ]
    assert list(d.index_iterator(start=1)) == [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
            ]
    assert list(d.index_iterator(start=0, stop=1)) == [(0, )]
    assert list(d.index_iterator(start=1, stop=2)) == [(0, ), (1, )]

def test_index_means():
    d = Data({
        (0, 0) : [0, 2]
    }, [1, 1, 2])

    assert d.mean(()) == 1
    assert d.mean((0, 0)) == 1
    assert d.mean((0, 0, 0)) == d[0, 0, 0]
    assert d.mean((0, 0, 1)) == d[0, 0, 1]

def test_index_means2():
    # Suppose we have three levels, so n = 3.
    # For the sake of example, level 1 is repetitions, level 2 is executions,
    # and level 3 is compilations. Now suppose we repeat level 3 twice,
    # level 2 twice and level 3 five times.
    #
    # This would be a valid data set:
    # Note that the indicies are off-by-one due to python indicies starting
    # from 0.
    d = Data({ (0, 0) : [ 3, 4, 4, 1, 2 ], # times for compile 1, execution 1
               (0, 1) : [ 3, 3, 3, 3, 3 ], # compile 1, execution 2
               (1, 0) : [ 1, 2, 3, 4, 5 ], # compile 2, execution 1
               (1, 1) : [ 1, 1, 4, 4, 1 ], # compile 2, execution 2
               }, [2, 2, 5]) # counts for each level (highest to lowest)

    # By calling mean with an empty tuple we compute the mean at all levels
    # i.e. the mean of all times:
    x = [3, 4, 4, 1, 2, 3, 3, 3, 3, 3, 1, 2, 3, 4, 5, 1, 1, 4, 4, 1]
    expect = sum(x)/float(len(x))
    assert expect == d.mean(())

    # By calling with a singleton tuple we compute the mean for a given
    #compilation. E.g. compilation 2
    x = [1, 2, 3, 4, 5, 1, 1, 4, 4, 1]
    expect = sum(x) / float(len(x))
    assert expect == d.mean((1,))

    # By calling with a pair we compute the mean for a given compile
    # and execution combo.
    # E.g. compile 1, execution 2, which is obviously a mean of 3.
    assert d.mean((0, 1)) == 3

def test_si2():
    d = Data({
        (0, 0) : [0, 0]
    }, [1, 1, 2])

    assert d.Si2(1) == 0

def test_si2_bigger_example():
    # Let's compute S_1^2 for the following data
    d = Data({
        (0, 0) : [3,4,3],
        (0, 1) : [1.2, 3.1, 3],
        (1, 0) : [0.2, 1, 1.5],
        (1, 1) : [1, 2, 3]
    }, [2, 2, 3])

    # So we have n = 3, r = (2, 2, 3)
    # By my reckoning we should get something close to 0.72667 (working below)
    # XXX Explanation from whiteboard need to go here XXX

    assert abs(d.Si2(1)-0.72667) <= 0.0001

def test_ti2():
    # To verify this, consider the following data:
    d = Data({
        (0, 0) : [3,4,3],
        (0, 1) : [1.2, 3.1, 3],
        (1, 0) : [0.2, 1, 1.5],
        (1, 1) : [1, 2, 3]
    }, [2, 2, 3])

    # Let's manually look at S_i^2 where 1 <= i <= n:
    #si_vec = [ d.Si2(i) for i in range(1, 4) ]
    #print(si_vec)

    ti_vec = [ d.Ti2(i) for i in range (1, 4) ]
    expect = [ 0.7266667, 0.262777778, 0.7747 ]

    for i in range(len(expect)):
        assert abs(ti_vec[i] - expect[i]) <= 0.0001

def test_optimal_reps_no_rounding():
    d = Data({
        (0, 0) : [3,4,3],
        (0, 1) : [1.2, 3.1, 3],
        (1, 0) : [0.2, 1, 1.5],
        (1, 1) : [1, 2, 3]
    }, [2, 2, 3])

    #ti_vec = [ d.Ti2(i) for i in range (1, 4) ]
    #print(ti_vec)

    # And suppose the costs (high level to low) are 100, 20 and 3 (seconds)
    # By my reckoning, the optimal repetition counts should be r_1 = 5, r_2 = 2
    # XXX show working XXX
    got = [d.optimalreps(i, (100, 20, 3), round=False) for i in [1,2]]
    expect = [4.2937, 1.3023]

    for i in range(len(got)):
        assert abs(got[i] - expect[i]) <= 0.001

    for i in got:
        assert type(i) == float

def test_optimal_reps_with_rounding():
    """ Same as test_optimal_reps_no_rounding() just with rounding."""

    d = Data({
        (0, 0) : [3,4,3],
        (0, 1) : [1.2, 3.1, 3],
        (1, 0) : [0.2, 1, 1.5],
        (1, 1) : [1, 2, 3]
    }, [2, 2, 3])

    got = [d.optimalreps(i, (100, 20, 3)) for i in [1,2]]
    expect = [5, 2]

    for i in range(len(got)):
        assert got[i] == expect[i]

    for i in got:
        assert type(i) == int

def test_worked_example_3_level():
    # three level experiment
    # This is the worked example from the paper.
    data = Data({
        (0, 0): [9., 5.], (0, 1): [8., 3.],
        (1, 0): [10., 6.], (1, 1): [7., 11.],
        (2, 0): [1., 12.], (2, 1): [2., 4.],
    }, [3, 2, 2])

    correct = {
            (0, 0): 7.0,
            (0, 1): 5.5,
            (1, 0): 8.0,
            (1, 1): 9.0,
            (2, 0): 6.5,
            (2, 1): 3.0,
    }

    for index in data.index_iterator(stop=2):
        assert data.mean(index) == correct[index]

    assert data.mean() == 6.5

    assert round(data.Si2(1), 1) == 16.5
    assert round(data.Si2(2), 1) == 2.6
    assert round(data.Si2(3), 1) == 3.6
    assert round(data.Ti2(1), 1) == 16.5
    assert round(data.Ti2(2), 1) == -5.7
    assert round(data.Ti2(3), 1) == 2.3

def test_worked_example_2_level():
    data = Data({
        (0, ): [9., 5., 8., 3.],
        (1, ): [10., 6., 7., 11.],
        (2, ): [1., 12., 2., 4.],
    }, [3, 4])

    correct = {(0, ): 6.3,
               (1, ): 8.5,
               (2, ): 4.8,
               }
    for index in data.index_iterator(stop=1):
        assert round(data.mean(index), 1) == correct[index]

    assert data.mean() == 6.5

    assert round(data.Si2(1), 1) == 12.7
    assert round(data.Si2(2), 1) == 3.6

    assert round(data.Ti2(1), 1) == 12.7
    assert round(data.Ti2(2), 1) == 0.4

def test_bootstrap():
    # XXX needs info on how expected val was computed
    data = Data({
            (0, ) : [ 2.5, 3.1, 2.7 ],
            (1, ) : [ 5.1, 1.1, 2.3 ],
            (2, ) : [ 4.7, 5.5, 7.1 ],
            }, [3, 3])
    random.seed(1)

    expect = 4.8111111111
    got = data.bootstrap_means(1) # one iteration

    assert abs(got[0] - expect) <= 0.0001

def test_confidence_slice_indicies():
    assert _confidence_slice_indicies(10, '0.8') == (1, (4, 5), 9)
    assert _confidence_slice_indicies(11, '0.8') == (1, (5, ), 10)
    assert _confidence_slice_indicies(1000) == (25, (499, 500), 975)

def test_confidence_slice():
    # Suppose we get back the means:
    means = [ x + 15 for x in range(1000) ] # already sorted

    # For a data set of size 1000, we expect alpha/2 to be 25
    # (for a 95% confidence interval)
    alpha_over_two = len(means) * 0.025
    assert(alpha_over_two) == 25

    # Therefore we lose 25 items off each end of the means list.
    # The first 25 indicies are 0, ..., 24, so lower bound should be index 25.
    # The last 25 indicies are -1, ..., -25, so upper bound is index -26
    # Put differently, the last 25 indicies are 999, ..., 975

    lower_index = int(math.floor(alpha_over_two))
    upper_index = int(-math.ceil(alpha_over_two) - 1)
    (lobo, hibo) = (means[lower_index], means[upper_index])

    # Since the data is the index plus 15, we should get an
    # interval: [25+15, 974+15]
    expect = (25+15, 974+15)
    assert (lobo, hibo) == expect

    # There is strictly speaking no median of 1000 items.
    # We take the mean of the two middle items items 500 and 501 at indicies
    # 499 and 500. Since the data is the index + 15, the middle values are
    # 514 and 515, the mean of which is 514.5
    median = 514.5

    # Check the implementation.
    confrange = confidence_slice(means)
    (got_lobo, got_median, got_hibo) = confrange
    assert confrange.lower == got_lobo
    assert confrange.median == got_median
    assert confrange.upper == got_hibo

    assert got_lobo == lobo
    assert got_hibo == hibo
    assert median == got_median

    assert confrange.error == _mean([median - lobo, hibo - median])


def test_confidence_slice_pass_confidence_level():
    means = [float(x) for x in range(10)]
    low, mean, high = confidence_slice(means, '0.8')
    assert mean == (4 + 5) / 2.
    assert low == 1
    assert high == 8


    means = [float(x) for x in range(11)]
    low, mean, high = confidence_slice(means, '0.8')
    assert mean == 5
    assert low == 1
    assert high == 9


def test_confidence_quotient():
    data1 = Data({
            (0, ) : [ 2.5, 3.1, 2.7 ],
            (1, ) : [ 5.1, 1.1, 2.3 ],
            (2, ) : [ 4.7, 5.5, 7.1 ],
            }, [3, 3])
    data2 = Data({
            (0, ) : [ 3.5, 4.1, 3.7 ],
            (1, ) : [ 6.1, 2.1, 3.3 ],
            (2, ) : [ 5.7, 6.5, 8.1 ],
            }, [3, 3])

    random.seed(1)
    a = data1._bootstrap_sample()
    b = data2._bootstrap_sample()

    random.seed(1)
    (_, mean, _) = data1.bootstrap_quotient(data2, iterations=1)
    assert mean == _mean(a) / _mean(b)

def test_confidence_quotient_div_zero():
    data1 = Data({
            (0, ) : [ 2.5, 3.1, 2.7 ],
            (1, ) : [ 5.1, 1.1, 2.3 ],
            (2, ) : [ 4.7, 5.5, 7.1 ],
            }, [3, 3])
    data2 = Data({ # This has a mean of zero
            (0, ) : [ 0, 0, 0],
            (1, ) : [ 0, 0, 0],
            (2, ) : [ 0, 0, 0],
            }, [3, 3])

    # Since all ratios will be +inf, the median should also be +inf
    (_, median, _) = data1.bootstrap_quotient(data2, iterations=1)
    assert median== float("inf")

def test_geomean():
    assert _geomean([10, 0.1]) == 1
