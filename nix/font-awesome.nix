{ sources ? null }:
let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
in

with pkgs;

stdenv.mkDerivation rec {
  pname = "font-awesome";
  version = "5.11.2";

  src = fetchFromGitHub {
    repo = "Font-Awesome";
    owner = "FortAwesome";
    rev = version;
    sha256 = "0ya14lgx5mgpjbnw6sss3a2c99n6cw6xryd0xj8rbjwbr2gmrf1q";
  };

  installPhase = ''
    mkdir -p $out/scss
    cp -r scss $out/scss/font-awesome
    cp -r webfonts $out
  '';
}
