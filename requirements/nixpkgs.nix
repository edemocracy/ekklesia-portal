let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "6326053490c70114656c0f04c0c894a249a7eab0";
    sha256 = "1z1v01k75s54r4vl2dsrxpfmdyn09j9lk4w1cp941mskyglmrg49";
  };
in import nixpkgs {}
