{ usePipenvShell ? false, sources ? import ./nix/sources.nix }:
let
  pkgs = import sources.nixpkgs { };
  niv = (import sources.niv { }).niv;
  lib = pkgs.lib;
  bandit = (import nix/bandit.nix { inherit pkgs; }).packages.bandit;
  installRequirements = import nix/install_requirements.nix { inherit pkgs; };
  devRequirements = import nix/dev_requirements.nix { inherit pkgs; };
  python = pkgs.python37.buildEnv.override {
    extraLibs = (builtins.attrValues devRequirements.packages) ++ 
                (builtins.attrValues installRequirements.packages);
    ignoreCollisions = true;
  };
  envVars = ''
    export PYTHONPATH=./src:../more.babel_i18n:../more.browser_session:${python}/${python.sitePackages}
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"; 
  '';

in pkgs.mkShell {
  name = "ekklesia_portal-dev-env";
  buildInputs = [
    bandit
    niv
    python
  ] ++
  (with pkgs; [ 
    cacert
    entr
    openssl.dev
    pipenv
    postgresql_11
    sassc
    zsh
  ]) ++
  (with pkgs.python37Packages; [
    autopep8
    ipdb
    mypy
    pip
    pip-tools
    pylint
    werkzeug
  ]) 
  ;
  shellHook = envVars + (lib.optionalString 
                         usePipenvShell "SHELL=`which zsh` exec pipenv shell --fancy");
}
