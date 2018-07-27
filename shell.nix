let
  pkgs = import ./requirements/nixpkgs.nix;
  pipenvCustom = pkgs.callPackage ./pipenv.nix {};
  pipenv = pkgs.pipenv;
in with pkgs; stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with python36Packages; [ sassc pyflakes pipenv zsh postgresql100 ];
  #shellHook = "PYTHONPATH= SHELL=`which zsh` pipenv shell --fancy";
}
