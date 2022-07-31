{ pkgs, default ? "unknown" }:

with builtins;
with pkgs;

let
  # Git complains about an "unsafe repository" without this global config.
  gitConf = pkgs.writeText "gitconfig-safedir-hack" ''
  [safe]
      directory = ${../.}
  '';
  gitVersion =
    lib.replaceStrings
      ["\n"]
      [""]
      (lib.readFile
        (runCommand
          "git-version" {
            src = ../.;
            buildInputs = [ gitMinimal ];
            GIT_CONFIG_GLOBAL = gitConf;
          }
          "cd $src; git describe --long --tags --dirty --always > $out"));
in
  if pathExists ../.git
  then gitVersion
  else default
