{ pipenv, python36Packages }:

pipenv.overrideAttrs(oldAttrs: rec {
  inherit (oldAttrs) pname;
  name = "${pname}-${version}";
  version = "2018.6.25";

  src = python36Packages.fetchPypi {
    inherit pname version;
    sha256 = "1sipsdka65pz3xg2kc8azmblalxssxh9rc0lnsnbqkmk73aw4xkw";
  };
})
