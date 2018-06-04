let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "7295e175bf6c6e8aa54f1b4d99256ee95d13d385";
    sha256 = "1h5d2nlyh4w4i51gihj7vs14pg8vaam3ks93250xv7brx978cy66";
  };
in import nixpkgs {}
