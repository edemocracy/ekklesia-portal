from pprint import pprint
from setuptools.config import read_configuration
conf = read_configuration('../setup.cfg')
options = conf['options']


with open('install_requirements.txt', 'w') as wf:
    wf.write('\n'.join(options['install_requires']))


with open('test_requirements.txt', 'w') as wf:
    wf.write('\n'.join(options['tests_require']))

