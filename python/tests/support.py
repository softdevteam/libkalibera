import os.path
import sys


# Allow to run out of source dir
def setup_paths():
    HERE = os.path.abspath(os.path.dirname(__file__))
    PARENT = os.path.join(HERE, "..")
    sys.path.append(PARENT)
