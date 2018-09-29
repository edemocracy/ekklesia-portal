let
  pkgs = import ./requirements/nixpkgs.nix;
in pkgs.stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with pkgs.python37Packages; [ pkgs.sassc pkgs.pipenv pkgs.zsh pkgs.postgresql100 python ];
  #shellHook = "PYTHONPATH= SHELL=`which zsh` pipenv shell --fancy";
}
