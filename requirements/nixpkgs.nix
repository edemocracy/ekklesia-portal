let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "dc7bddbb8927258644d90e914abd96776ef83a5b";
    sha256 = "0w67gcy7wpy6bihm0pkd4h2gr71g7kppsh0vkw71g7nn51i2yz5k";
  };
in import nixpkgs {}
