# Build Python package.
# Can be installed in the current user profile with:
# nix-env -if .
{ sources ? null }:
let
  deps = import ./nix/deps.nix { inherit sources; };
  pkgs = deps.pkgs;
  lib = pkgs.lib;
  version =
    lib.replaceStrings
      ["\n"]
      [""]
      (lib.readFile
        (pkgs.runCommand
          "git-version"
          { src = ./.; buildInputs = [ pkgs.gitMinimal ]; }
          "cd $src; git describe --long --tags --dirty --always > $out"));

in pkgs.python37Packages.buildPythonPackage rec {
  pname = "ekklesia-portal";
  name = "${pname}";
  src = pkgs.nix-gitignore.gitignoreSource [] ./.;
  doCheck = false;
  catchConflicts = false;

  propagatedBuildInputs = with deps;
    install ++
    dev ++
    debugLibsAndTools;


  passthru = {
    inherit deps;
    inherit (deps) python;
  };
}
