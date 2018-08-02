{ pkgs ? import ./requirements/nixpkgs.nix }:
let
  inherit (pkgs) lib pythonPackages;

  pythonPackageName = "ekklesia_portal";

  basename = path: with pkgs.lib; with builtins; last (splitString "/" path);
  src-filter = path: type: with pkgs.lib;
    let
      ext = last (splitString "." path);
    in
      !elem (basename path) [".git" "__pycache__" ".eggs" "result"] &&
      !elem ext ["egg-info" "pyc" "nix" ];

  src = builtins.filterSource src-filter ./.;
  python = import ./requirements/requirements.nix { inherit pkgs; };
  deps = builtins.attrValues python.packages ++ (lib.optional lib.inNixShell (with pkgs.python37Packages; [ ipython ipdb pkgs.sassc ]));

in python.mkDerivation rec {
  pname = pythonPackageName;
  name = "${pname}-${version}";
  version = lib.removeSuffix "\n" ( builtins.readFile ( ./. + "/src/${pythonPackageName}/VERSION" ) );
  inherit src;
  propagatedBuildInputs = deps;
  doCheck = false;
  passthru.deps = deps;
  passthru.env = python.interpreter.interpreter.withPackages ( ps: deps );
  passthru.interpreter = python.interpreter;
  passthru.pythonPackage = pythonPackageName;
  passthru.wsgiCallable = "app";
}
