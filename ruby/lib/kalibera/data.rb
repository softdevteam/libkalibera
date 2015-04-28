require "stringio"
require "base64"
require "rbzip2"
require "bigdecimal"
require "memoist"

module Kalibera

  CONSTANTS = RBzip2::Decompressor.new(StringIO.new(Base64.decode64("""\
  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
  NLhVQA=="""))).read.split().map { |x| Float(x) }

  # Look up the 95% quantile from constant table.
  def self.student_t_quantile95(ndeg)
    index = ndeg - 1
    if index >= CONSTANTS.size
      index = -1 # the quantile converges, we just take the last value
    end
    CONSTANTS[index]
  end

  ConfRange = Struct.new(:lower, :median, :upper) do
    def error
      Kalibera.mean([upper - median, median - lower])
    end
  end

  # Returns a tuples (lower, median, upper), where:
  # lower: lower bound of 95% confidence interval
  # median: the median value of the data
  # upper: uper bound of 95% confidence interval
  # 
  # Arguments:
  # means -- the list of means (need not be sorted).
  def self.confidence_slice(means, confidence="0.95")
    means = means.sort
    # There may be >1 median indicies, i.e. data is even-sized.
    lower, middle_indicies, upper = confidence_slice_indicies(means.size, confidence)
    median = mean(middle_indicies.map { |i| means[i] })
    ConfRange.new(means[lower], median, means[upper - 1]) # upper is *exclusive*
  end

  # Returns a triple (lower, mean_indicies, upper) so that l[lower:upper]
  # gives confidence_level of all samples. Mean_indicies is a tuple of one or
  # two indicies that correspond to the mean position
  #
  # Keyword arguments:
  # confidence_level -- desired level of confidence as a Decimal instance.
  def self.confidence_slice_indicies(length, confidence_level=BigDecimal.new('0.95'))
    raise unless !confidence_level.instance_of?(Float)
    confidence_level = BigDecimal.new(confidence_level)
    raise unless confidence_level.instance_of?(BigDecimal)
    exclude = (1 - confidence_level) / 2

    if length % 2 == 0
      mean_indicies = [length / 2 - 1, length / 2]  # TRANSLITERATION: was //
    else
      mean_indicies = [length / 2]  # TRANSLITERATION: was //
    end

    lower_index = Integer(
        (exclude * length).round(0, BigDecimal::ROUND_DOWN) # TRANSLITERATION: was quantize 1.
    )

    upper_index = Integer(
        ((1 - exclude) * length).round(0, BigDecimal::ROUND_UP) # TRANSLITERATION: was quantize 1.
    )

    [lower_index, mean_indicies, upper_index]
  end

  def self.mean(l)
    l.inject(0, :+) / Float(l.size)
  end

  def self.geomean(l)
    l.inject(1, :*) ** (1.0 / Float(l.size))
  end

  class Data

    extend Memoist

    # Instances of this class store measurements (corresponding to
    # the Y_... in the papers).
    #
    # Arguments:
    # data -- Dict mapping tuples of all but the last index to lists of values.
    # reps -- List of reps for each level, high to low.
    def initialize(data, reps)
      @data = data
      @reps = reps

      # check that all data is there

      array = reps.map { |i| (0...i).to_a }
      array[0].product(*array.drop(1)).each do |index|
        self[*index] # does not crash
      end
    end

    def [](*indicies)
      raise unless indicies.size == @reps.size
      x = @data[indicies[0...indicies.size-1]]
      raise unless !x.nil?
      x[indicies[-1]]
    end

    # Computes a list of all possible data indcies gievn that
    # start <= index <= stop are fixed.
    def index_iterator(start=0, stop=nil)
      if stop.nil?
        stop = n
      end

      maximum_indicies = @reps[start...stop]
      remaining_indicies = maximum_indicies.map { |maximum| (0...maximum).to_a }
      return [[]] if remaining_indicies.empty?
      remaining_indicies[0].product(*remaining_indicies.drop(1))
    end

    # The number of levels in the experiment.
    def n
      @reps.size
    end

    # The number of repetitions for level i.
    #
    # Arguments:
    # i -- mathematical index.
    def r(i)
      raise unless 1 <= i
      raise unless i <= n
      index = n - i
      @reps[index]
    end

    # Compute the mean across a number of values.
    #
    # Keyword arguments:
    # indicies -- tuple of fixed indicies over which to compute the mean,
    # given from left to right. The remaining indicies are variable.
    def mean(indicies=[])
      remaining_indicies_cross_product =
          index_iterator(start=indicies.size)
      alldata = remaining_indicies_cross_product.map { |remaining| self[*(indicies + remaining)] }
      Kalibera.mean(alldata)
    end

    memoize :mean

    # Biased estimator S_i^2.
    # 
    # Arguments:
    # i -- the mathematical index of the level from which to compute S_i^2
    def Si2(i)
      raise unless 1 <= i
      raise unless i <= n
      # @reps is indexed from the left to right
      index = n - i
      factor = 1.0

      # We compute this iteratively leveraging the fact that
      # 1 / (a * b) = (1 / a) / b
      for rep in @reps[0, index]
        factor /= rep
      end
      # Then at this point we have:
      # factor * (1 / (r_i - 1)) = factor / (r_i - 1)
      factor /=  @reps[index] - 1

      # Second line of the above definition, the lines are multiplied.
      indicies = index_iterator(0, index+1)
      sum = 0.0
      for index in indicies
        a = mean(index)
        b = mean(index[0,index.size-1])
        sum += (a - b) ** 2
      end
      factor * sum
    end

    memoize :Si2

    # Compute the unbiased T_i^2 variance estimator.
    # 
    # Arguments:
    # i -- the mathematical index from which to compute T_i^2.
    def Ti2(i)
      # This is the broken implementation of T_i^2 shown in the pubslished
      # version of "Rigorous benchmarking in reasonable time". Tomas has
      # since fixed this in local versions of the paper.
      #@memoize
      #def broken_Ti2(self, i)
      #  """ Compute the unbiased T_i^2 variance estimator.
      #
      #  Arguments:
      #  i -- the mathematical index from which to compute T_i^2.
      #  """
      #
      #  raise unless 1 <= i <= n
      #  if i == 1:
      #    return self.Si2(1)
      #  return self.Si2(i) - self.Ti2(i - 1) / self.r(i - 1)

      # This is the correct definition of T_i^2

      raise unless 1 <= i
      raise unless i <= n
      if i == 1
        return Si2(1)
      end
      Si2(i) - Si2(i - 1) / r(i - 1)
    end

    memoize :Ti2

    # Computes the optimal number of repetitions for a given level.
    #
    # Note that the resulting number of reps is not rounded.
    #
    # Arguments:
    # i -- the mathematical level of which to compute optimal reps.
    # costs -- A list of costs for each level, *high* to *low*.
    def optimalreps(i, costs)
      # NOTE: Does not round
      costs = costs.map { |x| Float(x) }
      raise unless 1 <= i
      raise unless i < n
      index = n - i
      return (costs[index - 1] / costs[index] *
          Ti2(i) / Ti2(i + 1)) ** 0.5
    end

    memoize :optimalreps

    # Compute the 95% confidence interval.
    def confidence95
      degfreedom = @reps[0] - 1
      student_t_quantile95(degfreedom) *
        (Si2(n) / @reps[0]) ** 0.5
    end

    # Compute a list of simulated means from bootstrap resampling.
    #
    # Note that, resampling occurs with replacement.
    #
    # Keyword arguments:
    # iterations -- Number of resamples (and thus means) generated.
    def bootstrap_means(iterations=1000)
      means = []
      for i in 0...iterations
        values = bootstrap_sample()
        means.push(Kalibera.mean(values))
      end
      means.sort()
      means
    end

    # Compute a 95% confidence interval via bootstrap method.
    #
    # Keyword arguments:
    # iterations -- Number of resamplings to base result upon.
    def bootstrap_confidence_interval(iterations=10000, confidence="0.95")
      means = bootstrap_means(iterations)
      confidence_slice(means, confidence)
    end

    def random_measurement_sample(index=[])
      results = []
      if index.size == n
        results.push self[*index]
      else
        indicies = (0...@reps[index.size]).map { |i| rand(@reps[index.size]) }
        for single_index in indicies
          newindex = index + [single_index]
          for value in random_measurement_sample(newindex)
            results.push value
          end
        end
      end
      results
    end

    def bootstrap_sample
      random_measurement_sample
    end

    def bootstrap_quotient(other, iterations=10000, confidence='0.95')
      ratios = []
      for _ in 0...iterations
        ra = bootstrap_sample()
        rb = other.bootstrap_sample()
        mean_ra = Kalibera.mean(ra)
        mean_rb = Kalibera.mean(rb)

        if mean_rb == 0 # protect against divide by zero
          ratios.push(Float::INFINITY)
        else
          ratios.push(mean_ra / mean_rb)
        end
      end
      ratios.sort!
      Kalibera.confidence_slice(ratios, confidence).values
    end

  end

  def self.bootstrap_geomean(l_data_a, l_data_b, iterations=10000, confidence='0.95')
    raise "lists need to match" unless l_data_a.size == l_data_b.size
    geomeans = []
    iterations.times do
      ratios = []
      l_data_a.zip(l_data_b).each do |a, b|
        ra = a.bootstrap_sample
        rb = b.bootstrap_sample
        mean_ra = mean(ra)
        mean_rb = mean(rb)
        ratios << mean_ra / mean_rb
      end
      geomeans << geomean(ratios)
    end
    geomeans.sort!
    confidence_slice(geomeans, confidence)
  end

end
