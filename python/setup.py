import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="libkalibera",  # XXX just 'kalibera'?
    version="0.1",  # XXX fetch from file
    author="Edd Barrett, Carl Friedrich Bolz",
    # author_email = "andrewjcarter@gmail.com",
    description=("Statistically rigorous benchmarking library"),
    license="MIT",
    keywords="benchmarks experiments statistics Kalibera Jones",
    url="http://soft-dev.org/src/libkalibera/",
    packages=['pykalibera'],  # XXX just 'kalibera'?
    long_description=read('../README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
)
