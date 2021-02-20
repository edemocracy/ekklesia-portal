{ sources ? null }:
with builtins;

let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
  niv = (import sources_.niv { }).niv;
  # Ekklesia-common is pulled in by poetry as Python dependency.
  # We don't use any Nix code from the project right now, so we don't have to import it here.
  # ekklesia-common = (import sources_.ekklesia-common { sources = sources_; });
  bootstrap = import ./bootstrap.nix { };
  javascriptDeps = import ./javascript_deps.nix { };
  font-awesome = import ./font-awesome.nix { };
  inherit ((import "${sources_.poetry2nix}/overlay.nix") pkgs pkgs) poetry2nix poetry;
  python = pkgs.python38;

  poetryWrapper = with python.pkgs; pkgs.writeScriptBin "poetry" ''
    export PYTHONPATH=
    unset SOURCE_DATE_EPOCH
    ${poetry}/bin/poetry "$@"
  '';

  overrides = poetry2nix.overrides.withDefaults (
    self: super: {
  });

in rec {
  inherit pkgs bootstrap javascriptDeps python;
  inherit (pkgs) lib sassc glibcLocales;
  inherit (python.pkgs) buildPythonApplication alembic gunicorn;

  mkPoetryApplication = { ... }@args:
    poetry2nix.mkPoetryApplication (args // {
      inherit overrides;
    });

  inherit (poetry2nix.mkPoetryPackages {
    projectDir = ../.;
    inherit python;
    inherit overrides;
  }) poetryPackages pyProject;

  poetryPackagesByName =
    lib.listToAttrs
      (map
        (p: { name = p.pname; value = p; })
        poetryPackages);

  inherit (poetryPackagesByName) deform babel;

  # Can be imported in Python code or run directly as debug tools
  debugLibsAndTools = with python.pkgs; [
    ipython
    poetryPackagesByName.pdbpp
  ];

  pythonDevTest = python.buildEnv.override {
    extraLibs = poetryPackages ++
                debugLibsAndTools;
    ignoreCollisions = true;
  };

  pythonTest = pythonDevTest;
  pythonDev = pythonDevTest;

  # Code style and security tools
  linters = with python.pkgs; let

    # Pylint needs to import the modules of our dependencies
    # but we don't want to override its own PYTHONPATH.
    setSysPath = ''
      import sys
      sys.path.append("${pythonDev}/${pythonDev.sitePackages}")
    '';

    pylintWrapper = with python.pkgs; pkgs.writeScriptBin "pylint" ''
      ${pylint}/bin/pylint --init-hook='${setSysPath}' "$@"
    '';

    isortWrapper = with python.pkgs; pkgs.writeScriptBin "isort" ''
      ${isort}/bin/isort --virtual-env=${pythonDev} "$@"
    '';

  in [
    bandit
    isortWrapper
    mypy
    pylintWrapper
    yapf
  ];

  # Various tools for log files, deps management, running scripts and so on
  shellTools = let
    ekklesiaPortalConsole = pkgs.writeScriptBin "ekklesia-portal-console" ''
      export PYTHONPATH=$PYTHONPATH:${pythonDev}/${pythonDev.sitePackages}
      ${python.pkgs.ipython}/bin/ipython -i consoleenv.py "$@"
    '';
  in [
    ekklesiaPortalConsole
    niv
    pkgs.entr
    pkgs.jq
    pkgs.postgresql_12
    pkgs.sassc
    pkgs.zsh
    poetryPackagesByName.eliot-tree
    poetryPackagesByName.pdbpp
    poetryWrapper
    python.pkgs.gunicorn
  ];


  # Needed for a development nix shell
  shellInputs =
    linters ++
    shellTools ++ [
      pythonTest
      bootstrap
    ];

  shellPath = lib.makeBinPath shellInputs;
  sassPath = "${bootstrap}/scss:${font-awesome}/scss";
  jsPath = "${javascriptDeps}/js";
  webfontsPath = "${font-awesome}/webfonts";
}
