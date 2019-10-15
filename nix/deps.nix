{ sources ? null }:
let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
  niv = (import sources_.niv { }).niv;
  bandit = (import ./bandit.nix { inherit pkgs; }).packages.bandit;
  eliotPkgs = (import ./eliot.nix { inherit pkgs; }).packages;
  lib = pkgs.lib;
  installRequirements = import ./install_requirements.nix { inherit pkgs; };
  devRequirements = import ./dev_requirements.nix { inherit pkgs; };

  setuptools = pkgs.python37Packages.setuptools;

in rec {
  inherit pkgs;

  gunicorn = pkgs.python37Packages.gunicorn.overrideAttrs(old: {
    propagatedBuildInputs = [ setuptools ];
  });

  # Can be imported in Python code or run directly as debug tools
  debugLibsAndTools = with pkgs.python37Packages; [
    ipdb
    ipython
  ];

  install = builtins.attrValues installRequirements.packages;
  dev = builtins.attrValues devRequirements.packages;

  python = pkgs.python37.buildEnv.override {
    extraLibs = install ++
                [ eliotPkgs.eliot setuptools ] ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  pythonDev = pkgs.python37.buildEnv.override {
    extraLibs = dev ++
                install ++
                [ eliotPkgs.eliot setuptools ] ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  # Code style and security tools
  linters = with pkgs.python37Packages; [
    bandit
    mypy
    pylama
    pylint
    autopep8
  ];

  # Various tools for log files, deps management, running scripts and so on
  shellTools = with pkgs; with python37Packages; [
    eliotPkgs.eliot-tree
    entr
    gunicorn
    jq
    niv
    openssl.dev
    pip
    postgresql_11
    uwsgi
    sassc
    zsh
  ];

  # Needed for a development nix shell
  shellInputs =
    [ pythonDev ] ++
    linters ++
    shellTools ++
    debugLibsAndTools;

  shellPath = lib.makeBinPath shellInputs;
}
