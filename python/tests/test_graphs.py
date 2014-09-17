import sys, os.path, random
import pytest

# Allow to run out of source dir
HERE = os.path.abspath(os.path.dirname(__file__))
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

# XXX Need to delete graphs
@pytest.fixture
def gpath():
    """ Returns a temp filename for graph storage """
    return  pytest.ensuretemp("graphs").join("graph.png").strpath

# ----------------------------------
# TESTS BEGIN
# ----------------------------------

def test_run_sequence(gpath, rdata):
    # Does not crash
    run_sequence_plot(rdata, filename=gpath)

def test_lag(gpath, rdata):
    # Does not crash
    lag_plot(rdata, filename=gpath)

def test_acr(gpath, rdata):
    # Does not crash
    acr_plot(rdata, filename=gpath)
