#!/bin/sh

pypi2nix -V python38 -e cookiecutter --basename cookiecutter
pypi2nix -V python38 -e pdbpp --basename pdbpp
pypi2nix -V python38 -e eliot-tree --basename eliot
