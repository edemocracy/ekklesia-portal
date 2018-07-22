# see setup.cfg for metadata and options; only requirements are loaded here
import os.path
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))


def find_version():
    with open(os.path.join(here, "src", "ekklesia_portal", "VERSION")) as version_file:
        return version_file.read().strip()


def read_install_requires():
    with open(os.path.join(here, "requirements", "install_requirements.txt")) as f:
        return [s.strip() for s in f.readlines()]


setup(install_requires=read_install_requires(),
      version=find_version(),
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      include_package_data=True,
      python_requires="~=3.6")
