{ pkgs, default ? "unknown" }:

with builtins;
with pkgs;

let
  gitVersion =
    lib.replaceStrings
      ["\n"]
      [""]
      (lib.readFile
        (runCommand
          "git-version"
          { src = ../.; buildInputs = [ gitMinimal ]; }
          "cd $src; git describe --long --tags --dirty --always > $out"));
in
  if pathExists ../.git
  then gitVersion
  else default
