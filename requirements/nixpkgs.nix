let 
  _systemNixpkgs = import <nixpkgs> {};
  nixpkgs = _systemNixpkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "362be9608c3e0dc5216e9d1d5f5c1a5643b7f7b1";
    sha256 = "0934rhanamsnhawg15gg6cy9ird3c47hsqn5s46lq2n5kzl6v7ly";
  };
in import nixpkgs {}
