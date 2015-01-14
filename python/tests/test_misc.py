import sys, os.path, random
import pytest

# Allow to run out of source dir
HERE = os.path.abspath(os.path.dirname(__file__))
PARENT = os.path.join(HERE, "..")
sys.path.append(PARENT)

from pykalibera.data import Data

def test_memoise_decor_docstrs():
    prefix = "Computes the optimal number of repetitions"
    assert Data.optimalreps.__doc__.startswith(prefix)
