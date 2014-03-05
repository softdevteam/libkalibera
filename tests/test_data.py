import sys, os.path, random
import pytest

# Allow to run out of source dir
HERE = os.path.abspath(os.path.curdir)
PARENT = os.path.join(HERE, "..")
sys.path.append(PARENT)
from pykalibera.graphs import run_sequence_plot, lag_plot, acr_plot

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

# XXX
