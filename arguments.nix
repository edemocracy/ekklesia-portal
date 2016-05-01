{ pkgs, pythonPackages }:

let
  p = builtins.trace;

  elem = builtins.elem;
  basename = path: with pkgs.lib; last (splitString "/" path);

  src-filter = path: type: with pkgs.lib;
    let
      ext = last (splitString "." path);
    in
      !elem (basename path) [".git" "__pycache__" ".eggs" "result"] &&
      !elem ext ["egg-info" "pyc"];

  arguments-src = builtins.filterSource src-filter ./.;

  self = pythonPackages // deps;

  gen_deps = (scopedImport {
    super = pythonPackages;
    inherit pkgs self;
    inherit (pkgs) fetchurl fetchgit;
  } ./python-packages.nix);

  overrides = rec {
    psycopg2 = gen_deps.psycopg2.override (attrs: {
      propagatedBuildInputs = [pkgs.postgresql];
    });

    #uwsgi = gen_deps.uwsgi.override (attrs: {
    #  buildInputs = [pkgs.ncurses];
    #});

    setuptools = pythonPackages.setuptools;

    setuptools-scm = pkgs.buildPythonPackage {
      name = "setuptools-scm-1.7.0";
      src = pkgs.fetchurl {
        url = "https://pypi.python.org/packages/source/s/setuptools_scm/setuptools_scm-1.7.0.tar.gz";
        md5 = "d0423feeabda9c6a869d963cdc397d64";
      };  
      doCheck = false;
    }; 

    misaka = pythonPackages.buildPythonPackage {
      name = "misaka-2.0.0";
      src = pkgs.fetchurl {
        url = "https://pypi.python.org/packages/source/m/misaka/misaka-2.0.0.tar.gz";
        md5 = "79352edb71f604402277d8bb6d3a54ef";
      };  
      doCheck = false;
      propagatedBuildInputs = with self; [ pythonPackages.cffi ];
    }; 

    Flask-Misaka = pythonPackages.buildPythonPackage {
      name = "Flask-Misaka-0.4.1";
      src = pkgs.fetchurl {
        url = "https://pypi.python.org/packages/source/F/Flask-Misaka/Flask-Misaka-0.4.1.tar.gz";
        md5 = "3bfbe604a6e3718b29b2b8bece137198";
      };  
      doCheck = false;
      buildInputs = with self; [ misaka flask ];
    }; 
  };

  deps = gen_deps // overrides;
  
  lib = pkgs.lib;
  
  nixpkgsDeps = lib.optionals lib.inNixShell [ pythonPackages.ipdb pythonPackages.ipython ];

  fullDeps = builtins.attrValues deps ++ nixpkgsDeps;

  arguments = pythonPackages.buildPythonPackage rec {
    propagatedBuildInputs = fullDeps;
    name = "arguments-0.0.1";
    src = arguments-src;
  };

  argumentsenv = pythonPackages.python.buildEnv.override {
    extraLibs = fullDeps;
    ignoreCollisions = true;
  };

in { inherit arguments; inherit argumentsenv; }
