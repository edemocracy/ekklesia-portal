#!/bin/sh

pushd python_requirements
# pin requirements and their versions
pip-compile install_requirements.txt -o frozen_install_requirements.txt
pip-compile dev_requirements.txt -o frozen_dev_requirements.txt

popd
pushd nix

# create nix requirements from intermediary pinned requirements
pypi2nix -V python37 -r ../python_requirements/frozen_install_requirements.txt \
  --basename install_requirements \
  -E postgresql -E libffi -E openssl.dev

pypi2nix -V python37 -r ../python_requirements/frozen_dev_requirements.txt \
  --basename dev_requirements

popd
