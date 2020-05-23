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
  inherit ((import "${sources_.poetry2nix}/overlay.nix") pkgs pkgs) poetry2nix poetry;
  python = pkgs.python38;
  overrides = poetry2nix.overrides.withDefaults (
    self: super: {
      psycopg2 = super.psycopg2.overridePythonAttrs (
        old: rec {
          nativeBuildInputs = with pkgs; [
            postgresql_12
            openssl
          ];
          buildInputs = nativeBuildInputs;
        }
      );
    });

in rec {
  inherit pkgs bootstrap javascriptDeps ekklesia-common python;
  inherit (pkgs) lib sassc glibcLocales;
  inherit (python.pkgs) buildPythonApplication gunicorn;

  mkPoetryApplication = { ... }@args:
    poetry2nix.mkPoetryApplication args // {
      inherit overrides;
    };

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
    pdbpp
  ];

  devLibs = [
    cookiecutter
  ];

  pythonDevTest = python.buildEnv.override {
    extraLibs = poetryPackages ++
                [ekklesia-common] ++
                debugLibsAndTools ++
                devLibs;
    ignoreCollisions = true;
  };

  pythonTest = pythonDevTest;
  pythonDev = pythonDevTest;

  # Code style and security tools
  linters = with python.pkgs; [
    bandit
    mypy
    pylama
    pylint
    autopep8
    yapf
  ];

  # Various tools for log files, deps management, running scripts and so on
  shellTools = with pkgs; with python.pkgs; [
    eliotPkgs.eliot-tree
    entr
    gunicorn
    jq
    niv
    poetry
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
