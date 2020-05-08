{ sources ? null }:
with builtins;

let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
  niv = (import sources_.niv { }).niv;
  ekklesia-common = (import sources_.ekklesia-common { sources = sources_; });
  bootstrap = import ./bootstrap.nix { };
  javascriptDeps = import ./javascript_deps.nix { };
  font-awesome = import ./font-awesome.nix { };
  eliotPkgs = (import ./eliot.nix { inherit pkgs; }).packages;
  pdbpp = (import ./pdbpp.nix { inherit pkgs; }).packages.pdbpp;
  cookiecutter = (import ./cookiecutter.nix { inherit pkgs; }).packages.cookiecutter;
  installPkgs = (import ./install_requirements.nix { inherit pkgs; }).packages;
  testPkgs = (import ./test_requirements.nix { inherit pkgs; }).packages;

  pythonPackages = pkgs.python38Packages;
  setuptools = pythonPackages.setuptools;

  # Adds missing dependency on setuptools for Python packages
  fixSetuptools = pkg: pkg.overrideAttrs(
    attrs: {
      propagatedBuildInputs = attrs.propagatedBuildInputs ++ [ setuptools ];
    });

in rec {
  inherit pkgs bootstrap javascriptDeps ekklesia-common;
  inherit (pkgs) lib sassc;
  inherit (installPkgs) babel deform;
  inherit (pythonPackages) buildPythonApplication;
  buildPythonEnv = pkgs.python38.buildEnv;

  gunicorn = (fixSetuptools pythonPackages.gunicorn);

  # Can be imported in Python code or run directly as debug tools
  debugLibsAndTools = with pythonPackages; [
    ipython
    pdbpp
  ];

  devLibs = with pythonPackages; [
    cookiecutter
  ];

  testLibs = (attrValues testPkgs) ++ [ setuptools ];

  installLibs = (attrValues installPkgs) ++ [
    eliotPkgs.eliot
    ekklesia-common
  ];

  python = buildPythonEnv.override {
    extraLibs = installLibs;
    ignoreCollisions = true;
  };

  pythonDevTest = buildPythonEnv.override {
    extraLibs = testLibs ++
                installLibs ++
                debugLibsAndTools ++
                devLibs;
    ignoreCollisions = true;
  };

  pythonTest = pythonDevTest;
  pythonDev = pythonDevTest;

  # Code style and security tools
  linters = with pythonPackages; [
    bandit
    mypy
    (fixSetuptools pylama)
    pylint
    autopep8
    yapf
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
    postgresql_12
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
