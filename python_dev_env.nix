#!/usr/bin/env -S nix-build -o pyenv
# Provides linters and a Python interpreter with runtime dependencies and test tools.
# Used for IDE integration (tested with VSCode, Pycharm).
# Run this file with ./python_dev_env.nix.
# It creates a directory 'pyenv' that is similar to a Python virtualenv.
# The 'pyenv' should be picked up py IDE as a possible project interpreter (restart may be required).
{ sources ? null }:
let
 deps = import ./nix/deps.nix { inherit sources; };
 pkgs = deps.pkgs;

in pkgs.buildEnv {
  name = "ekklesia-portal-dev-env";
  paths = with deps;
    [ pythonDev ] ++
    linters;
}
