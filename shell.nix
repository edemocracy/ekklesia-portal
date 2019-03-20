{ usePipenvShell ? true }:
let
  pkgs = import ./requirements/nixpkgs.nix;
  # pipenv = pkgs.callPackage ./requirements/pipenv.nix { inherit pkgs; };
in pkgs.stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with pkgs.python37Packages; [ pkgs.sassc pkgs.pipenv pkgs.zsh pkgs.postgresql_11 python ];
  shellHook = if usePipenvShell then "PYTHONPATH= SHELL=`which zsh` exec pipenv shell --fancy" else "export PYTHONPATH=";
}
