import math, itertools, random

import bz2

constants = bz2.decompress("""\
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
NLhVQA==""".decode("base64"))

constants = [float(x) for x in constants.split()]

def student_t_quantile95(ndeg):
    """Look up the 95% quantile from constant table."""
    index = ndeg - 1
    if index >= len(constants):
        index = -1 # the quantile converges, we just take the last value
    return constants[index]

def confidence_slice(means, confidence="0.95"):
    """Returns a tuples (lower, median, upper), where:
    lower: lower bound of 95% confidence interval
    median: the median value of the data
    upper: uper bound of 95% confidence interval

    Arguments:
    means -- the list of means (need not be sorted).
    """

    means = sorted(means)
    # There may be >1 median indicies, i.e. data is even-sized.
    lower, middle_indicies, upper = _confidence_slice_indicies(len(means), confidence)
    median = _mean([means[i] for i in middle_indicies])
    return means[lower], median, means[upper - 1] # upper is *exclusive*

def memoize(func):
    """ The @memoize decorator """
    attr = "%s_%s" % (func.func_name, id(func))
    def memoized(self, *args, **kwargs):
        d = self._memoization_values
        key = attr, args
        try:
            return d[key]
        except KeyError:
            res = d[key] = func(self, *args, **kwargs)
            return res
    return memoized

# Used for index calculation to not get weird float effects.
# We actually saw some of these effects in our exerimentation.
from decimal import Decimal, ROUND_UP, ROUND_DOWN

def _confidence_slice_indicies(length, confidence_level=Decimal('0.95')):
    """Returns a triple (lower, mean_indicies, upper) so that l[lower:upper]
    gives confidence_level of all samples. Mean_indicies is a tuple of one or
    two indicies that correspond to the mean position

    Keyword arguments:
    confidence_level -- desired level of confidence as a Decimal instance.
    """

    assert not isinstance(confidence_level, float)
    confidence_level = Decimal(confidence_level)
    assert isinstance(confidence_level, Decimal)
    exclude = (1 - confidence_level) / 2

    if length % 2 == 0:
        mean_indicies = (length // 2 - 1, length // 2)
    else:
        mean_indicies = (length // 2, )

    lower_index = int(
            (exclude * length).quantize(Decimal('1.'), rounding=ROUND_DOWN)
    )

    upper_index = int(
            ((1 - exclude) * length).quantize(Decimal('1.'), rounding=ROUND_UP)
    )

    return lower_index, mean_indicies, upper_index

def _mean(l):
    return math.fsum(l) / float(len(l))

# ---

class Data(object):
    def __init__(self, data, reps):
        """Instances of this class store measurements (corresponding to
        the Y_... in the papers).

        Arguments:
        data -- Dict mapping tuples of all but the last index to lists of values.
        reps -- List of reps for each level, high to low.
        """

        self.data = data
        self.reps = reps

        self._memoization_values = {}
        # check that all data is there
        for index in itertools.product(*[range(i) for i in reps]):
            self[index] # does not crash

    def __getitem__(self, indicies):
        assert len(indicies) == len(self.reps)
        return self.data[indicies[:-1]][indicies[-1]]

    def index_iterator(self, start=0, stop=None):
        """Computes a list of all possible data indcies gievn that
        start <= index <= stop are fixed."""

        if stop is None:
            stop = self.n

        maximum_indicies = self.reps[start:stop]
        remaining_indicies = [range(maximum) for maximum in maximum_indicies]
        return itertools.product(*remaining_indicies)

    @property
    def n(self):
        """The number of levels in the experiment."""
        return len(self.reps)

    def r(self, i):
        """The number of repetitions for level i.

        Arguments:
        i -- mathematical index.
        """
        assert 1 <= i <= self.n
        index = self.n - i
        return self.reps[index]

    @memoize
    def mean(self, indicies=()):
        """Compute the mean across a number of values.

        Keyword arguments:
        indicies -- tuple of fixed indicies over which to compute the mean,
        given from left to right. The remaining indicies are variable."""

        remaining_indicies_cross_product = \
                self.index_iterator(start=len(indicies))
        alldata = [self[indicies + remaining] \
                for remaining in remaining_indicies_cross_product]
        return _mean(alldata)

    @memoize
    def Si2(self, i):
        """Biased estimator S_i^2.

        Arguments:
        i -- the mathematical index of the level from which to compute S_i^2
        """
        assert 1 <= i <= self.n
        # self.reps is indexed from the left to right
        index = self.n - i
        factor = 1.0

        # We compute this iteratively leveraging the fact that
        # 1 / (a * b) = (1 / a) / b
        for rep in self.reps[:index]:
            factor /= rep
        # Then at this point we have:
        # factor * (1 / (r_i - 1)) = factor / (r_i - 1)
        factor /=  self.reps[index] - 1

        # Second line of the above definition, the lines are multiplied.
        indicies = self.index_iterator(stop=index+1)
        sum = 0.0
        for index in indicies:
            a = self.mean(index)
            b = self.mean(index[:-1])
            sum += (a - b) ** 2
        return factor * sum

    @memoize
    def Ti2(self, i):
        """Compute the unbiased T_i^2 variance estimator.

        Arguments:
        i -- the mathematical index from which to compute T_i^2.
        """

        assert 1 <= i <= self.n
        if i == 1:
            return self.Si2(1)
        # Note: in the "Rigorous benchmarking in reasonable time", the
        # expression belown was incorrectly shown as being equivalent to:
        #   return self.Si2(i) - self.Ti2(i - 1) / self.r(i - 1)
        # This has since been corrected in a revised version of the paper, and
        # we use the revised version below.
        return self.Si2(i) - self.Si2(i - 1) / self.r(i - 1)

    @memoize
    def optimalreps(self, i, costs, round=True):
        """Computes the optimal number of repetitions for a given level.

        Arguments:
        i -- the mathematical level of which to compute optimal reps.
        costs -- A list of costs for each level, *high* to *low*.
        round -- When True, the result is rounded (up) to an integral number
                 of repetitions.
        """

        costs = [ float(x) for x in costs ]
        assert 1 <= i < self.n
        index = self.n - i
        res_f =  (costs[index - 1] / costs[index] * \
                  self.Ti2(i) / self.Ti2(i + 1)) ** 0.5
        return int(math.ceil(res_f)) if round else res_f

    def confidence95(self):
        """Compute the 95% confidence interval."""

        degfreedom = self.reps[0] - 1
        return student_t_quantile95(degfreedom) * \
            (self.Si2(self.n) / self.reps[0]) ** 0.5

    def bootstrap_means(self, iterations=1000):
        """Compute a list of simulated means from bootstrap resampling.

        Note that, resampling occurs with replacement.

        Keyword arguments:
        iterations -- Number of resamples (and thus means) generated.
        """
        means = []
        for i in range(iterations):
            values = self._bootstrap_sample()
            means.append(_mean(values))
        means.sort()
        return means

    def bootstrap_confidence_interval(self, iterations=10000, confidence="0.95"):
        """Compute a 95% confidence interval via bootstrap method.

        Keyword arguments:
        iterations -- Number of resamplings to base result upon.
        """

        means = self.bootstrap_means(iterations)
        return confidence_slice(means, confidence)

    def _bootstrap_sample(self):
        # Uses a closure to mimic the abritrary nested loop depth construct
        # shown in the paper "Quantifying performance changes with effect
        # size confidence intervals".
        def _random_measurement_sample(index=()):
            if len(index) == self.n:
                yield self[index]
            else:
                indicies = [random.randrange(self.reps[len(index)]) \
                        for i in range(self.reps[len(index)])]
                for single_index in indicies:
                    newindex = index + (single_index, )
                    for value in _random_measurement_sample(newindex):
                        yield value
        return list(_random_measurement_sample())

    def bootstrap_quotient(self, other, iterations=10000, confidence='0.95'):
        ratios = []
        for _ in range(iterations):
            ra = self._bootstrap_sample()
            rb = other._bootstrap_sample()
            mean_ra = _mean(ra)
            mean_rb = _mean(rb)

            if mean_rb == 0: # protect against divide by zero
                ratios.append(float("inf"))
            else:
                ratios.append(mean_ra / mean_rb)
        ratios.sort()
        return confidence_slice(ratios, confidence)
