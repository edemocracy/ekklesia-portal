{ pipenv, python36Packages }:

pipenv.overrideAttrs(oldAttrs: rec {
  inherit (oldAttrs) pname;
  name = "${pname}-${version}";
  version = "11.0.2";

  src = python36Packages.fetchPypi {
    inherit pname version;
    sha256 = "0qqnbsryj8ihjkalbyfvhpjj237sgq9yv1ra6fwjc2mhg18cp5h7";
  };
})
