#!/bin/sh
pushd requirements
# lock packages and create requirements files with pinned versions and hashes
pipenv lock -r | sort > pypi2nix_source_deps_with_hash # contains all dependencies (no dev deps)

# strip hashes and filter out self-dependency -e . 
awk '{ if ($1!="-e") print $1 }' pypi2nix_source_deps_with_hash | grep -v '\-e .' > pypi2nix_source_deps
# create requirements.nix from intermediary pypi2nix_source_deps
pypi2nix -I nixpkgs=$HOME/git/nixpkgs -V 3.7 -r pypi2nix_source_deps -E postgresql -E libffi
popd
