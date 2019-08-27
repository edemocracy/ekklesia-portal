{ sources ? import ./nix/sources.nix }:
let
  pkgs = import sources.nixpkgs { };
  niv = (import sources.niv { }).niv;
  lib = pkgs.lib;
  bandit = (import nix/bandit.nix { inherit pkgs; }).packages.bandit;
  eliotTree = (import nix/eliot_tree.nix { inherit pkgs; }).packages.eliot-tree;
  installRequirements = import nix/install_requirements.nix { inherit pkgs; };
  devRequirements = import nix/dev_requirements.nix { inherit pkgs; };
  python = pkgs.python37.buildEnv.override {
    extraLibs = (builtins.attrValues devRequirements.packages) ++ 
                (builtins.attrValues installRequirements.packages);
    ignoreCollisions = true;
  };

in pkgs.buildEnv {
  name = "ekklesia_portal-dev";
  paths = [
    bandit
    eliotTree
    niv
    python
  ];
}
