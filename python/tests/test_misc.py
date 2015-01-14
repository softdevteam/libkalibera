import support

support.setup_paths()

from pykalibera.data import Data


def test_memoise_decor_docstrs():
    prefix = "Computes the optimal number of repetitions"
    assert Data.optimalreps.__doc__.startswith(prefix)
