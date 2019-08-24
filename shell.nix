{ usePipenvShell ? false }:
let
  pkgs = import ./requirements/nixpkgs.nix;
  lib = pkgs.lib;
  bandit = (import requirements/bandit.nix { inherit pkgs; }).packages.bandit;
  envVars = ''
    export PYTHONPATH=./src:../more.babel_i18n:../more.browser_session:$PYTHONPATH
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"; 
  '';

in pkgs.stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  propagatedBuildInputs = with pkgs; [ 
    bandit
    cacert
    entr
    openssl.dev
    pipenv
    postgresql_11
    sassc
    zsh
  ] ++
  (with python37Packages; [
    autopep8
    ipdb
    mypy
    pip
    pip-tools
    pylint
    python 
    werkzeug
  ]);
  shellHook = envVars + (lib.optionalString 
                         usePipenvShell "SHELL=`which zsh` exec pipenv shell --fancy");
}
