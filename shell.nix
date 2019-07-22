{ usePipenvShell ? true }:
let
  pkgs = import ./requirements/nixpkgs.nix;
in pkgs.stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with pkgs; [ 
    entr
    pipenv
    postgresql_11
    python37Packages.python 
    sassc
    zsh
  ];
  shellHook = if usePipenvShell then "PYTHONPATH= SHELL=`which zsh` exec pipenv shell --fancy" else "export PYTHONPATH=";
}
