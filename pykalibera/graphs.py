class GraphError(Exception): pass

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def run_sequence_plot(data, title="Run sequence plot", filename=None,
        xlabel="Run #", ylabel="Time(s)"):
    """Plots a run sequence graph.

    Arguments:
    data -- list of data points

    Keyword arguments:
    title -- graph title
    filename -- filename to write graph to (None plots to screen)
    xlabel -- label on x-axis"
    ylabel -- label on y-axis"
    """
    xs = range(len(data))

    plt.cla()
    p = plt.plot(xs, data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

def lag_plot(data, lag=5, filename=None,
        title=None, xlabel="Lag time(s)", ylabel="Time(s)"):
    """Generates a lag plot.

    Arguments:
    data -- list of data points

    Keyword arguments:
    lag -- which lag to plot
    filename -- filename to write graph to (None plots to screen)
    title -- graph title
    xlabel -- label on x-axis
    ylabel -- label on y-axis
    """

    # Python's index operator allows correct wrapping if lag index
    # is less than zero.
    xs = [ data[x-lag] for x in range(len(data)) ]

    plt.cla()
    p = plt.plot(xs, data, 'rx')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

def acr_plot(data, filename=None, title="ACR Plot",
        xlabel="Lag #", ylabel="Correlation"):
    """Generates an ACF plot, demeaned and normalised.

    Arguments:
    data -- list of data points

    Keyword arguments:
    filename -- filename to write graph to (None plots to screen)
    title -- graph title
    xlabel -- label on x-axis
    ylabel -- label on y-axis
    """

    # de-mean the data
    #mean = sum(data) / float(len(data))
    #xs = [ x - mean for x in data ]

    plt.cla()
    plt.acorr(data, detrend=mlab.detrend_mean, usevlines=True,
            maxlags=None, normed=True, lw=2)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()
