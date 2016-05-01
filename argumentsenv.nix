args @ { pkgs ? (import <nixpkgs> {}), pythonPackages ? pkgs.python35Packages }:
builtins.trace args
(import ./arguments.nix {inherit pkgs pythonPackages; }).argumentsenv

