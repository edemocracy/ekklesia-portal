{ sources ? null, system ? builtins.currentSystem }:
with builtins;

let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  poetry2nixSrc = "${sources_.poetry2nix}";
  # Taken from overlay.nix from poetry2nix, adapted for python310
  pkgs = import sources_.nixpkgs {
    overlays = [(final: prev: {
      poetry2nix = import poetry2nixSrc { pkgs = final; poetry = final.poetry; };
      poetry = prev.callPackage "${poetry2nixSrc}/pkgs/poetry" { python = final.python310; };
    })];
  };

  inherit (pkgs) poetry poetry2nix stdenv lib;
  niv = (import sources_.niv { }).niv;
  # Ekklesia-common is pulled in by poetry as Python dependency.
  # We don't use any Nix code from the project right now, so we don't have to import it here.
  # ekklesia-common = (import sources_.ekklesia-common { sources = sources_; });
  bootstrap = import ./bootstrap.nix { };
  javascriptDeps = import ./javascript_deps.nix { };
  font-awesome = import ./font-awesome.nix { };
  python = pkgs.python310;

  overrides = poetry2nix.overrides.withDefaults (
    self: super:
    let
      pythonBuildDepNameValuePair = deps: pname: {
        name = pname;
        value = super.${pname}.overridePythonAttrs (old: {
          buildInputs = old.buildInputs ++ deps;
        });
      };

      addPythonBuildDeps = deps: pnames:
        lib.listToAttrs
          (map
            (pythonBuildDepNameValuePair deps)
            pnames);
    in
    {
      macfsevents = super.macfsevents.overridePythonAttrs (
        old: {
          buildInputs =
            old.buildInputs
            ++ lib.optionals stdenv.isDarwin [ pkgs.darwin.apple_sdk.frameworks.CoreServices ];
        }
      );

      pypugjs = super.pypugjs.overridePythonAttrs (
        old: {
          format = "setuptools";
          buildInputs = old.buildInputs ++ [ poetry ];
        }
      );
    } //
    (addPythonBuildDeps
      [ self.flit-core ]
      [ "pyparsing" "markdown-it-py" ]) //
    (addPythonBuildDeps
      [ self.poetry ]
      [ "ekklesia-common" "iso8601" "mimesis-factory" "pytest-factoryboy" ]) //
    (addPythonBuildDeps
      [ self.pbr ]
      [ "munch" ]) //
    (addPythonBuildDeps
      [ self.hatchling ]
      [ "soupsieve" ])
  );

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
        (p: { name = p.pname or "none"; value = p; })
        poetryPackages);

in rec {
  inherit bootstrap javascriptDeps mkPoetryApplication pkgs poetryPackagesByName python;
  inherit (pkgs) lib sassc glibcLocales;
  inherit (python.pkgs) gunicorn;
  inherit (poetryPackagesByName) alembic deform ekklesia-common babel;

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
    pkgs.niv
    pkgs.entr
    pkgs.jq
    pkgs.postgresql_13
    pkgs.sassc
    pkgs.zsh
    poetryPackagesByName.eliot-tree
    poetryPackagesByName.pdbpp
    poetry
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
