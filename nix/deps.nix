{ sources ? null }:
with builtins;

let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
  niv = (import sources_.niv { }).niv;
  bandit = (import ./bandit.nix { inherit pkgs; }).packages.bandit;
  bootstrap = import ./bootstrap.nix { };
  javascriptDeps = import ./javascript_deps.nix { };
  font-awesome = import ./font-awesome.nix { };
  eliotPkgs = (import ./eliot.nix { inherit pkgs; }).packages;
  pdbpp = (import ./pdbpp.nix { inherit pkgs; }).packages.pdbpp;
  installPkgs = (import ./install_requirements.nix { inherit pkgs; }).packages;
  testPkgs = (import ./test_requirements.nix { inherit pkgs; }).packages;
  pythonPackages = pkgs.python37Packages;
  setuptools = pythonPackages.setuptools;


in rec {
  inherit pkgs bootstrap javascriptDeps;
  inherit (pkgs) lib sassc;
  inherit (installPkgs) babel deform;
  inherit (pythonPackages) buildPythonApplication;
  buildPythonEnv = pkgs.python37.buildEnv;

  gunicorn = pythonPackages.gunicorn.overrideAttrs(old: {
    propagatedBuildInputs = [ setuptools ];
  });

  # Can be imported in Python code or run directly as debug tools
  debugLibsAndTools = with pythonPackages; [
    ipython
    pdbpp
  ];

  testLibs = (attrValues testPkgs) ++ [ setuptools ];

  installLibs = (attrValues installPkgs) ++ [
    eliotPkgs.eliot
  ];

  python = buildPythonEnv.override {
    extraLibs = installLibs;
    ignoreCollisions = true;
  };

  pythonTest = buildPythonEnv.override {
    extraLibs = testLibs ++
                installLibs ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  pythonDev = pythonTest;

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
    [ pythonTest bootstrap ] ++
    linters ++
    shellTools ++
    debugLibsAndTools;

  shellPath = lib.makeBinPath shellInputs;
  sassPath = "${bootstrap}/scss:${font-awesome}/scss";
  jsPath = "${javascriptDeps}/js";
  webfontsPath = "${font-awesome}/webfonts";
}
