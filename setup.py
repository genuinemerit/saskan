#!python

"""
Saskantinon Applications

New simplified setup.py.
See setup.cfg for detailed build metadata.
setuptools will read setup.cfg to build the package.
See lab:old_setup.py for previous install instructions.
Goals are:
- Use a makefile and standard kind of make instructions
  to configure, build, and install.
- Create a package that can be installed with pip.
- Deploy to PyPI.
"""
from setuptools import setup

setup(
    version="0.1.1.0"
)
