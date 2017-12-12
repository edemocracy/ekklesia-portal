# overwrites requirements/install_requirements.txt without asking!
# must be run from the root directory

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = sorted(convert_deps_to_pip(pfile['packages'], r=False))

with open("requirements/install_requirements.txt", "w") as wf:
    for line in requirements:
        wf.write(line + "\n")
