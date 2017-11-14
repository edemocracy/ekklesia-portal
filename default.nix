{ nixpkgs ? (import ./requirements/nixpkgs.nix) }:
let 
pkgs = import nixpkgs {};
arguments = import ./requirements/arguments.nix { inherit pkgs; };
in arguments
