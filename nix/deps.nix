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
      psycopg2 = super.psycopg2.overridePythonAttrs (
        old: rec {
          nativeBuildInputs = with pkgs; [
            postgresql_12
            openssl
          ];
          buildInputs = nativeBuildInputs;
        }
      );
      # Project needs poetry to build. Is this an error in poetry2nix?
      ekklesia-common = super.ekklesia-common.overridePythonAttrs (
        old: rec {
          buildInputs = [ poetry ];
        }
      );
    });

in rec {
  inherit pkgs bootstrap javascriptDeps python;
  inherit (pkgs) lib sassc glibcLocales;
  inherit (python.pkgs) buildPythonApplication gunicorn;

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
  linters = with python.pkgs; [
    bandit
    mypy
    pylama
    pylint
    yapf
  ];

  # Various tools for log files, deps management, running scripts and so on
  shellTools = [
    niv
    pkgs.entr
    pkgs.jq
    pkgs.postgresql_12
    pkgs.sassc
    pkgs.zsh
    poetryPackagesByName.eliot-tree
    poetryWrapper
    python.pkgs.gunicorn
  ];


  # Needed for a development nix shell
  shellInputs =
    linters ++
    shellTools ++
    debugLibsAndTools ++ [
      pythonTest
      bootstrap
    ];

  shellPath = lib.makeBinPath shellInputs;
  sassPath = "${bootstrap}/scss:${font-awesome}/scss";
  jsPath = "${javascriptDeps}/js";
  webfontsPath = "${font-awesome}/webfonts";
}
