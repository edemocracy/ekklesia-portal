let 
  fetchNixpkgs = import ./fetchNixpkgs.nix;
  nixpkgs = fetchNixpkgs {
    rev = "eac38d0b1e68b4ae4f0b78fe778b61d0f314ae7a";
    sha256 = "00fcaga6802dkc5ikcfm3vwbqpaspqi5j626lmnmpqi6zc5x9ibc";
  };
in import nixpkgs {}
