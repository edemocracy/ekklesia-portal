# see setup.cfg for metadata and options; only requirements are loaded here
import os.path
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))


def read_install_requires():
    with open(os.path.join(here, "python_requirements/install_requirements.txt")) as f:
        return [s.strip() for s in f.readlines()]


setup(install_requires=read_install_requires(),
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      include_package_data=True,
      python_requires="~=3.7")
