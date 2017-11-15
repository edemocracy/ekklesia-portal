from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def find_version():
    with open(os.path.join(here, "arguments", "VERSION")) as version_file:
        return version_file.read().strip()


def read_requirements_file(requirements_type):
    with open(os.path.join(here, "requirements", requirements_type + "_requirements.txt")) as f:
        return [s.strip() for s in f.readlines()]


setup(
    name="arguments",
    version=find_version(),
    description="arguments",
    # The project URL.
    url="",
    author='dpausp',
    author_email='dpausp@posteo.de',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database'
    ],
    keywords='arguments ekklesia evoting edemocracy democracy',
    packages=find_packages(),
    install_requires=read_requirements_file("install"),
    setup_requires=read_requirements_file("setup"),
    tests_require=read_requirements_file("test"),
    extras_require = {
        "devel": read_requirements_file("devel")
    },
    python_requires="~=3.6",
    include_package_data=True,
)
