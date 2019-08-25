#!/bin/sh
pushd generated_requirements

# pin requirements and their versions
pip-compile install_requirements.txt -o frozen_install_requirements.txt
pip-compile dev_requirements.txt -o frozen_dev_requirements.txt

popd
pushd nix

# create nix requirements from intermediary pinned requirements
pypi2nix -V 3.7 -r ../generated_requirements/frozen_install_requirements.txt \
  -E postgresql -E libffi --basename install_requirements

pypi2nix -V 3.7 -r ../generated_requirements/frozen_dev_requirements.txt \
  --basename dev_requirements

popd
