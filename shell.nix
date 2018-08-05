let
  pkgs = import ./requirements/nixpkgs.nix;
  pipenv = pkgs.pipenv;
in with pkgs; stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with python37Packages; [ sassc pyflakes pipenv zsh postgresql100 python ];
  #shellHook = "PYTHONPATH= SHELL=`which zsh` pipenv shell --fancy";
}
