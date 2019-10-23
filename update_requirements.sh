#!/bin/sh

pushd python_requirements
python create_requirement_files.py
pushd nix

pypi2nix -V python37 -r ../python_requirements/install_requirements.txt \
  --basename install_requirements \
  -E postgresql -E libffi -E openssl.dev

pypi2nix -V python37 -r ../python_requirements/test_requirements.txt \
  --basename test_requirements

popd
