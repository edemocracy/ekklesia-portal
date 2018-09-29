let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "c5668bd18356391cd09e79d0465c4a4f3fe4a10a";
    sha256 = "0v5095835g8s0xszsqwmn1a48az5aba2581snljzjgy32zd3gxcb";
  };
in import nixpkgs {}
