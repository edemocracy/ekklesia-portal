#!/usr/bin/env python

import os
import shutil

shutil.move('tests/{{cookiecutter.concept_name}}', '../../../../tests/concepts/')
os.rmdir('tests')
