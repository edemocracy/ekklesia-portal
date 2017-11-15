# see setup.cfg for metadata and options; only requirements are loaded here
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)

from setuptools import setup
setup(install_requires=requirements)