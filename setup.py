# see setup.cfg for metadata and options; only requirements are loaded here
import os.path


here = os.path.abspath(os.path.dirname(__file__))


def read_install_requires():
    with open(os.path.join(here, "requirements", "install_requirements.txt")) as f:
        return [s.strip() for s in f.readlines()]


from setuptools import setup
setup(install_requires=read_install_requires())
