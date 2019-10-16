{ sources ? null }:
let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
  niv = (import sources_.niv { }).niv;
  bandit = (import ./bandit.nix { inherit pkgs; }).packages.bandit;
  bootstrap = import ./bootstrap.nix { };
  eliotPkgs = (import ./eliot.nix { inherit pkgs; }).packages;
  installRequirements = import ./install_requirements.nix { inherit pkgs; };
  devRequirements = import ./dev_requirements.nix { inherit pkgs; };
  pythonPackages = pkgs.python37Packages;
  setuptools = pythonPackages.setuptools;

in rec {
  inherit pkgs;
  inherit (pkgs) lib;
  inherit (pythonPackages) buildPythonPackage;
  buildPythonEnv = pkgs.python37.buildEnv;

  gunicorn = pythonPackages.gunicorn.overrideAttrs(old: {
    propagatedBuildInputs = [ setuptools ];
  });

  # Can be imported in Python code or run directly as debug tools
  debugLibsAndTools = with pythonPackages; [
    ipdb
    ipython
  ];

  install = builtins.attrValues installRequirements.packages;
  dev = builtins.attrValues devRequirements.packages;

  python = buildPythonEnv.override {
    extraLibs = install ++
                [ eliotPkgs.eliot setuptools ] ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  pythonDev = buildPythonEnv.override {
    extraLibs = dev ++
                install ++
                [ eliotPkgs.eliot setuptools ] ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  # Code style and security tools
  linters = with pythonPackages; [
    bandit
    mypy
    pylama
    pylint
    autopep8
  ];

  # Various tools for log files, deps management, running scripts and so on
  shellTools = with pkgs; with pythonPackages; [
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
    [ pythonDev bootstrap ] ++
    linters ++
    shellTools ++
    debugLibsAndTools;

  shellPath = lib.makeBinPath shellInputs;
  sassPath = "${bootstrap}/scss";
}
