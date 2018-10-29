let
  pkgs = import ./requirements/nixpkgs.nix;
  pipenv = (pkgs.pipenv.override { python3Packages = pkgs.python37Packages; }).overrideAttrs(oldAttrs: {
    name = "pipenv-2018.10.28";
    src = pkgs.fetchFromGitHub {
      owner = "pypa";
      repo = "pipenv";
      rev = "e8bf34b5481a368211e757ea5cae66f10b3077e1";
      sha256 = "1np49ghkk33b13hwiqalprhcxawc3qxjc0dm5bf9wc3578q8jfrq";
    };
  });

in pkgs.stdenv.mkDerivation {
  src = null;
  name = "ekklesia_portal-dev-env";
  phases = [];
  buildInputs = with pkgs.python37Packages; [ pkgs.sassc pipenv pkgs.zsh pkgs.postgresql100 python ];
  shellHook = "export PYTHONPATH=";
  #shellHook = SHELL=`which zsh` pipenv shell --fancy";
}
