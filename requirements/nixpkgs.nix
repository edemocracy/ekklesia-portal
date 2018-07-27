let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "ba1a04367d0c60362106afab290d9334f3232b48";
    sha256 = "1n787pkl3m7m0sw81h02qd69s2r7pm54jh9j6cw5pdaridgka9l1";
  };
in import nixpkgs {}
