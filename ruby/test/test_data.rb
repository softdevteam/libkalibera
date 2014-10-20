require "test/unit"

require "kalibera"

# We need to match Python's random numbers when testing

class TestData < Kalibera::Data

  RAND = [0, 2, 2, 0, 1, 1, 1, 2, 0, 0, 2, 1, 2, 0, 1, 2, 0, 2, 2, 0, 0, 1,
          2, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 2, 1, 1, 0, 2, 2, 0, 0]

  def initialize(data, reps)
    super
    @rand_counter = 0
  end

  def reset_local_rand
    @rand_counter = 0
  end

  def rand(r)
    raise "mock rand designed for range=3" unless r == 3
    raise "mock rand out of data" unless @rand_counter < RAND.size

    n = RAND[@rand_counter]
    @rand_counter += 1
    n
  end

end

class TestKaliberaData < Test::Unit::TestCase

  def test_indicies
    d = TestData.new({
      [0, 0] => [1, 2, 3, 4, 5],
      [0, 1] => [3, 4, 5, 6, 7]
      }, [1, 2, 5])

    assert_equal 1, d[0, 0, 0]
    assert_equal 5, d[0, 0, 4]
    assert_equal 5, d[0, 1, 2]
  end

  def test_rep_levels
    d = TestData.new({
      [0, 0] => [1, 2, 3, 4, 5],
      [0, 1] => [3, 4, 5, 6, 7]
      }, [1, 2, 5])

    assert_equal 5, d.r(1) # lowest level, i.e. arity of the lists in the map
    assert_equal 2, d.r(2)
    assert_equal 1, d.r(3)

    # indexs are one based, so 0 or less is invalid
    assert_raise RuntimeError do
      d.r(0)
    end

    assert_raise RuntimeError do
      d.r(-1337)
    end

    # Since we have 3 levels here, levels 4 and above are bogus
    assert_raise RuntimeError do
      d.r(4)
    end

    assert_raise RuntimeError do
      d.r(666)
    end
  end

  def test_index_iter
    d = TestData.new({
      [0, 0] => [1, 2, 3, 4, 5],
      [0, 1] => [3, 4, 5, 6, 7]
      }, [1, 2, 5])

    assert_equal [
        [0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4],
        [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3], [0, 1, 4],
        ], d.index_iterator()
    assert_equal [
        [0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
        [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
        ], d.index_iterator(start=1)
    assert_equal [[0]], d.index_iterator(start=0, stop=1)
    assert_equal [[0], [1]], d.index_iterator(start=1, stop=2)
  end

  def test_index_means
    d = TestData.new({
      [0, 0] => [0, 2]
    }, [1, 1, 2])

    assert_equal 1, d.mean([])
    assert_equal 1, d.mean([0, 0])
    assert_equal d[0, 0, 0], d.mean([0, 0, 0])
    assert_equal d[0, 0, 1], d.mean([0, 0, 1])
  end

  def test_index_means2
    # Suppose we have three levels, so n = 3.
    # For the sake of example, level 1 is repetitions, level 2 is executions,
    # and level 3 is compilations. Now suppose we repeat level 3 twice,
    # level 2 twice and level 3 five times.
    #
    # This would be a valid data set:
    # Note that the indicies are off-by-one due to python indicies starting
    # from 0.
    d = TestData.new({ [0, 0] => [ 3, 4, 4, 1, 2 ], # times for compile 1, execution 1
           [0, 1] => [ 3, 3, 3, 3, 3 ], # compile 1, execution 2
           [1, 0] => [ 1, 2, 3, 4, 5 ], # compile 2, execution 1
           [1, 1] => [ 1, 1, 4, 4, 1 ], # compile 2, execution 2
           }, [2, 2, 5]) # counts for each level (highest to lowest)

    # By calling mean with an empty tuple we compute the mean at all levels
    # i.e. the mean of all times:
    x = [3, 4, 4, 1, 2, 3, 3, 3, 3, 3, 1, 2, 3, 4, 5, 1, 1, 4, 4, 1]
    expect = x.inject(0, :+)/Float(x.size)
    assert_equal d.mean([]), expect

    # By calling with a singleton tuple we compute the mean for a given
    #compilation. E.g. compilation 2
    x = [1, 2, 3, 4, 5, 1, 1, 4, 4, 1]
    expect = x.inject(0, :+) / Float(x.size)
    assert_equal d.mean([1]), expect

    # By calling with a pair we compute the mean for a given compile
    # and execution combo.
    # E.g. compile 1, execution 2, which is obviously a mean of 3.
    assert_equal 3, d.mean([0, 1])
  end

  def test_si2
    d = TestData.new({
      [0, 0] => [0, 0]
    }, [1, 1, 2])

    assert_equal 0, d.Si2(1)
  end

  def test_si2_bigger_example
    # Let's compute S_1^2 for the following data
    d = TestData.new({
      [0, 0] => [3,4,3],
      [0, 1] => [1.2, 3.1, 3],
      [1, 0] => [0.2, 1, 1.5],
      [1, 1] => [1, 2, 3]
    }, [2, 2, 3])

    # So we have n = 3, r = (2, 2, 3)
    # By my reckoning we should get something close to 0.72667 (working below)
    # XXX Explanation from whiteboard need to go here XXX

    assert_less_equal (d.Si2(1)-0.72667).abs, 0.0001
  end

  def test_ti2
    # To verify this, consider the following data:
    d = TestData.new({
      [0, 0] => [3,4,3],
      [0, 1] => [1.2, 3.1, 3],
      [1, 0] => [0.2, 1, 1.5],
      [1, 1] => [1, 2, 3]
    }, [2, 2, 3])

    # Let's manually look at S_i^2 where 1 <= i <= n:
    #si_vec = [ d.Si2(i) for i in range(1, 4) ]
    #print(si_vec)

    ti_vec = (1...4).map { |i| d.Ti2(i) }
    expect = [ 0.7266667, 0.262777778, 0.7747 ]

    (0...expect.size).each do |i|
      assert (ti_vec[i] - expect[i]).abs <= 0.0001, "#{} <= 0.0001"
    end
  end

  def test_optimal_reps
    d = TestData.new({
      [0, 0] => [3,4,3],
      [0, 1] => [1.2, 3.1, 3],
      [1, 0] => [0.2, 1, 1.5],
      [1, 1] => [1, 2, 3]
    }, [2, 2, 3])

    #ti_vec = [ d.Ti2(i) for i in range (1, 4) ]
    #print(ti_vec)

    # And suppose the costs (high level to low) are 100, 20 and 3 (seconds)
    # By my reckoning, the optimal repetition counts should be r_1 = 5, r_2 = 2
    # XXX show working XXX
    got = [1,2].map { |i|d.optimalreps(i, [100, 20, 3]) }
    expect = [4.2937, 1.3023]

    (0...got.size).each do |i|
      assert_less_equal (got[i] - expect[i]).abs, 0.001
    end
  end

  def test_worked_example_3_level
    # three level experiment
    # This is the worked example from the paper.
    data = TestData.new({
      [0, 0] => [9.0, 5.0], [0, 1] => [8.0, 3.0],
      [1, 0] => [10.0, 6.0], [1, 1] => [7.0, 11.0],
      [2, 0] => [1.0, 12.0], [2, 1] => [2.0, 4.0],
    }, [3, 2, 2])

    correct = {
        [0, 0] => 7.0,
        [0, 1] => 5.5,
        [1, 0] => 8.0,
        [1, 1] => 9.0,
        [2, 0] => 6.5,
        [2, 1] => 3.0,
    }

    data.index_iterator(0, 2).each do |index|
      assert data.mean(index) == correct[index]
    end

    assert_equal 6.5, data.mean()

    assert_equal 16.5, data.Si2(1).round(1)
    assert_equal 2.6, data.Si2(2).round(1)
    assert_equal 3.6, data.Si2(3).round(1)
    assert_equal 16.5, data.Ti2(1).round(1)
    assert_equal -5.7, data.Ti2(2).round(1)
    assert_equal 2.3, data.Ti2(3).round(1)
  end

  def test_worked_example_2_level
    data = TestData.new({
      [0] => [9.0, 5.0, 8.0, 3.0],
      [1] => [10.0, 6.0, 7.0, 11.0],
      [2] => [1.0, 12.0, 2.0, 4.0],
    }, [3, 4])

    correct = {[0] => 6.3,
           [1] => 8.5,
           [2] => 4.8,
           }
    data.index_iterator(0, 1).each do |index|
      assert data.mean(index).round(1) == correct[index]
    end

    assert_equal 6.5, data.mean()

    assert_equal 12.7, data.Si2(1).round(1)
    assert_equal 3.6, data.Si2(2).round(1)

    assert_equal 12.7, data.Ti2(1).round(1)
    assert_equal 0.4, data.Ti2(2).round(1)
  end

  def test_bootstrap
    # XXX needs info on how expected val was computed
    data = TestData.new({
        [0] => [ 2.5, 3.1, 2.7 ],
        [1] => [ 5.1, 1.1, 2.3 ],
        [2] => [ 4.7, 5.5, 7.1 ],
        }, [3, 3])
    data.reset_local_rand

    expect = 4.8111111111
    got = data.bootstrap_means(1) # one iteration

    assert_less_equal (got[0] - expect).abs, 0.0001
  end

  def test_confidence_slice_indicies
    assert_equal [1, [4, 5], 9], Kalibera.confidence_slice_indicies(10, '0.8')
    assert_equal [1, [5], 10], Kalibera.confidence_slice_indicies(11, '0.8')
    assert_equal [25, [499, 500], 975], Kalibera.confidence_slice_indicies(1000)
  end

  def test_confidence_slice
    # Suppose we get back the means:
    means = (0...1000).map { |x| x + 15 } # already sorted

    # For a data set of size 1000, we expect alpha/2 to be 25
    # (for a 95% confidence interval)
    alpha_over_two = means.size * 0.025
    assert(alpha_over_two) == 25

    # Therefore we lose 25 items off each end of the means list.
    # The first 25 indicies are 0, ...0, 24, so lower bound should be index 25.
    # The last 25 indicies are -1, ...0, -25, so upper bound is index -26
    # Put differently, the last 25 indicies are 999, ...0, 975

    lower_index = Integer(alpha_over_two.floor)
    upper_index = Integer(-alpha_over_two.ceil - 1)
    lobo, hibo = [means[lower_index], means[upper_index]]

    # Since the data is the index plus 15, we should get an
    # interval: [25+15, 974+15]
    expect = [25+15, 974+15]
    assert_equal expect, [lobo, hibo]

    # There is strictly speaking no median of 1000 items.
    # We take the mean of the two middle items items 500 and 501 at indicies
    # 499 and 500. Since the data is the index + 15, the middle values are
    # 514 and 515, the mean of which is 514.5
    median = 514.5

    # Check the implementation.
    got_lobo, got_median, got_hibo = Kalibera.confidence_slice(means)

    assert_equal lobo, got_lobo
    assert_equal hibo, got_hibo
    assert_equal got_median, median
  end

  def test_confidence_slice_pass_confidence_level
    means = (0...10).map { |x| Float(x) }
    low, mean, high = Kalibera.confidence_slice(means, '0.8')
    assert_equal (4 + 5) / 2.0, mean
    assert_equal 1, low
    assert_equal 8, high


    means = (0...11).map { |x| Float(x) }
    low, mean, high = Kalibera.confidence_slice(means, '0.8')
    assert_equal 5, mean
    assert_equal 1, low
    assert_equal 9, high
  end

  def test_confidence_quotient
    data1 = TestData.new({
        [0] => [ 2.5, 3.1, 2.7 ],
        [1] => [ 5.1, 1.1, 2.3 ],
        [2] => [ 4.7, 5.5, 7.1 ],
        }, [3, 3])
    data2 = TestData.new({
        [0] => [ 3.5, 4.1, 3.7 ],
        [1] => [ 6.1, 2.1, 3.3 ],
        [2] => [ 5.7, 6.5, 8.1 ],
        }, [3, 3])

    data1.reset_local_rand
    data2.reset_local_rand
    a = data1.bootstrap_sample()
    b = data2.bootstrap_sample()

    data1.reset_local_rand
    data2.reset_local_rand
    _, mean, _ = data1.bootstrap_quotient(data2, iterations=1)
    assert_equal Kalibera.mean(a) / Kalibera.mean(b), mean
  end

  def test_confidence_quotient_div_zero
    data1 = TestData.new({
        [0] => [ 2.5, 3.1, 2.7 ],
        [1] => [ 5.1, 1.1, 2.3 ],
        [2] => [ 4.7, 5.5, 7.1 ],
        }, [3, 3])
    data2 = TestData.new({ # This has a mean of zero
        [0] => [ 0, 0, 0],
        [1] => [ 0, 0, 0],
        [2] => [ 0, 0, 0],
        }, [3, 3])

    # Since all ratios will be +inf, the median should also be +inf
    _, median, _ = data1.bootstrap_quotient(data2, iterations=1)
    assert_equal Float::INFINITY, median
  end

  def assert_less_equal(x, y)
    assert x <= y, "#{x.inspect} <= #{y.inspect}"
  end

end
