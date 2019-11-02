{ pkgs }:
with builtins;
with pkgs;

lib.replaceStrings
  ["\n"]
  [""]
  (lib.readFile
    (runCommand
      "git-version"
      { src = ../.; buildInputs = [ gitMinimal ]; }
      "cd $src; git describe --long --tags --dirty --always > $out"))
