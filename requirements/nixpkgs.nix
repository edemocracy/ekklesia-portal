let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "bea4b361a0e3a21b1e9a69d56f1ebd16fb38a296";
    sha256 = "0ybslsfvib4lrq6vj5mibmpjvwcd5xljjr2zp23zmihcjvc4d1r9";
  };
in import nixpkgs {}
