{ sources ? null }:
let
  sources_ = if (sources == null) then import ./sources.nix else sources;
  pkgs = import sources_.nixpkgs { };
in

with pkgs;

stdenv.mkDerivation rec {
  pname = "bootstrap";
  version = "4.3.1";

  src = fetchFromGitHub {
    repo = "bootstrap";
    owner = "twbs";
    rev = "v${version}";
    sha256 = "18g76r53sa2ahcriy7jk5wvxd3s8qc4as87xwqvfkxibdn5ifrxs";
  };

  installPhase = ''
    mkdir -p $out/scss
    cp -r scss $out/scss/bootstrap
    cp -r dist/js $out
  '';
}
