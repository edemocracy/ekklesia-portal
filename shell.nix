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
                (builtins.attrValues installRequirements.packages) ++
                [ pkgs.python37Packages.ipython ];
    ignoreCollisions = true;
  };
  inputs = [
    bandit
    eliotTree
    niv
    python
  ] ++
  (with pkgs; [ 
    cacert
    entr
    jq
    openssl.dev
    pipenv
    postgresql_11
    sassc
    zsh
  ]) ++
  (with pkgs.python37Packages; [
    autopep8
    ipdb
    mypy
    pip
    pip-tools
    pylint
    werkzeug
  ]);

  path = lib.makeBinPath inputs;

in pkgs.mkShell {
  name = "ekklesia_portal-dev-env";
  buildInputs = inputs;
  shellHook = ''
    export PYTHONPATH=./src
    export PATH=${path}
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"; 
  '';
}
