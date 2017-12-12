#!/usr/bin/env sh
# Removing the nspkg.pth files for the more namespace package fixes the problem that more.babel_i18n (editable install) cannot be found.
# We don't need them on Python >=3.3.

venv=`pipenv --venv`
pushd $venv/lib/python3.6/site-packages
rm -vf more.*nspkg.pth
popd
