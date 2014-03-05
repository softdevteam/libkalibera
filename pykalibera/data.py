import math, itertools, random, csv

def confidence_slice_95(means):
    """Returns a tuples (lower, median, upper), where:
    lower: lower bound of 95% confidence interval
    median: the median value of the data
    upper: uper bound of 95% confidence interval

    Arguments:
    means -- the list of means (need not be sorted).
    """

    means = sorted(means)
    lower, mean_indicies, upper = _confidence_slice_indicies(len(means))
    mean = _mean([means[i] for i in mean_indicies])
    return means[lower], mean, means[upper - 1] # upper is *exclusive*

def memoize(func):
    """ The @memoize decorator """
    attr = "%s_%s" % (func.func_name, id(func))
    def memoized(self, *args):
        d = self._memoization_values
        key = attr, args
        try:
            return d[key]
        except KeyError:
            res = d[key] = func(self, *args)
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
                for remaining in remaining_indcies_cross_product]
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

    # This is the broken implementation of T_i^2 shown in the pubslished
    # version of "Rigorous benchmarking in reasonable time". Tomas has
    # since fixed this in local versions of the paper.
    #@memoize
    #def broken_Ti2(self, i):
    #    """ Compute the unbiased T_i^2 variance estimator.
    #
    #    Arguments:
    #    i -- the mathematical index from which to compute T_i^2.
    #    """
    #
    #    assert 1 <= i <= self.n
    #    if i == 1:
    #        return self.Si2(1)
    #    return self.Si2(i) - self.Ti2(i - 1) / self.r(i - 1)

    # This is the correct definition of T_i^2
    @memoize
    def Ti2(self, i):
        """Compute the unbiased T_i^2 variance estimator.

        Arguments:
        i -- the mathematical index from which to compute T_i^2.
        """

        assert 1 <= i <= self.n
        if i == 1:
            return self.Si2(1)
        return self.Si2(i) - self.Si2(i - 1) / self.r(i - 1)

    # NOTE: Does not round
    @memoize
    def optimalreps(self, i, costs):
        """Computes the optimal number of repetitions for a given level.

        Note that the resulting number of reps is not rounded.

        Arguments:
        i -- the mathematical level of which to compute optimal reps.
        costs -- A list of costs for each level, XXX high to low? XXX.
        """

        costs = [ float(x) for x in costs ]
        assert 1 <= i < self.n
        index = self.n - i
        return (costs[index - 1] / costs[index] * \
                self.Ti2(i) / self.Ti2(i + 1)) ** 0.5

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

        means = []
        for i in range(iterations):
            values = list(_random_measurement_sample())
            means.append(_mean(values))
        return means

    def bootstrap_confidence_interval(self, iterations=10000):
        """Compute a 95% confidence interval via bootstrap method.

        Keyword arguments:
        iterations -- Number of resamplings to base result upon.
        """

        means = self.bootstrap_means(iterations)
        return confidence_slice_95(means, iterations)
