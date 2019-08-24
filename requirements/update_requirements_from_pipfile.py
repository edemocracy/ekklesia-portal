# overwrites requirements/{install,dev}_requirements.txt without asking!
# must be run from the root directory

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = sorted(convert_deps_to_pip(pfile['packages'], r=False))
dev_requirements = sorted(convert_deps_to_pip(pfile['dev-packages'], r=False))

with open("requirements/install_requirements.txt", "w") as wf:
    for line in requirements:
        wf.write(line + "\n")

with open("requirements/dev_requirements.txt", "w") as wf:
    for line in dev_requirements:
        if not line.startswith("-e ."):
            wf.write(line + "\n")
