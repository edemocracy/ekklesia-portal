#!/bin/sh
pushd requirements
# lock packages and create requirements files with pinned versions and hashes
pipenv lock -r | sort > all_deps # contains all dependencies
pipenv lock -r -d | sort > dev_deps # contains only deps from [dev-packages]

# only use deps which are in all_deps, but not in dev_deps
comm -23 all_deps dev_deps > pypi2nix_source_deps_with_hash

# strip hashes and filter out self-dependency -e . 
awk '{ if ($1!="-e") print $1 }' pypi2nix_source_deps_with_hash | grep -v '\-e .' > pypi2nix_source_deps
# create requirements.nix from intermediary pypi2nix_source_deps
pypi2nix -V 3.6 -r pypi2nix_source_deps -E postgresql -E libffi
popd