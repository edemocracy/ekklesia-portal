#!/bin/sh
pushd requirements
# lock packages and create requirements files with pinned versions
pipenv lock -r > pypi2nix_source_deps # contains all dependencies (no dev deps)
# create requirements.nix from intermediary pypi2nix_source_deps
pypi2nix -I nixpkgs=$HOME/git/nixpkgs -V 3.7 -r pypi2nix_source_deps -E postgresql -E libffi
popd
