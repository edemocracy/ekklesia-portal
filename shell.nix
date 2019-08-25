{ usePipenvShell ? false, sources ? import ./nix/sources.nix }:
let
  pkgs = import sources.nixpkgs { };
  niv = (import sources.niv { }).niv;
  lib = pkgs.lib;
  bandit = (import nix/bandit.nix { inherit pkgs; }).packages.bandit;
  installRequirements = import nix/install_requirements.nix { inherit pkgs; };
  devRequirements = import nix/dev_requirements.nix { inherit pkgs; };
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
    niv
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
  ]) ++ (builtins.attrValues devRequirements.packages)
  ++ (builtins.attrValues installRequirements.packages)
  ;
  shellHook = envVars + (lib.optionalString 
                         usePipenvShell "SHELL=`which zsh` exec pipenv shell --fancy");
}
