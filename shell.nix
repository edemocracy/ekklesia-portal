let
  pkgs = import ./requirements/nixpkgs.nix;

in with pkgs; stdenv.mkDerivation {
  src = null;
  name = "arguments-dev-env";
  phases = [];
  buildInputs = with python36Packages; [ sassc ipython ipdb pyflakes pipenv zsh ];
  shellHook = "SHELL=`which zsh` pipenv shell --fancy";
}

