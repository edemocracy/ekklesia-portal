{ nixpkgs ? (import ./nixpkgs.nix) }:
let
pkgs = import nixpkgs {};
arguments = import ./arguments.nix { inherit pkgs; };
in arguments.interpreter

