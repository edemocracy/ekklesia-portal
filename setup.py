from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="arguments",
    version=find_version('arguments', '__init__.py'),
    description="arguments",
    # The project URL.
    url="",
    # Author details
    author='dpausp',
    author_email='dpausp@posteo.de',
    # Choose your license
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database'
    ],
    keywords='arguments ekklesia evoting edemocracy democracy',
    packages=["arguments",
              "arguments.views",
              "arguments.views.admin",
              ],
    install_requires=[],
    setup_requires=["setuptools-git"],
    include_package_data=True,
)
