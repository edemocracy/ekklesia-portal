# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python37 -e bandit --basename bandit
#

{ pkgs ? import <nixpkgs> {},
  overrides ? ({ pkgs, python }: self: super: {})
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python37;
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python37-interpreter";
        buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter} \
              $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "
              (selectPkgsFn pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -x "$prog" ] && [ -f "$prog" ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          ln -s ${pythonPackages.python.executable} \
              python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };

      interpreter = interpreterWithPackages builtins.attrValues;
    in {
      __old = pythonPackages;
      inherit interpreter;
      inherit interpreterWithPackages;
      mkDerivation = args: pythonPackages.buildPythonPackage (args // {
        nativeBuildInputs = (args.nativeBuildInputs or []) ++ args.buildInputs;
      });
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (
          drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; }
        );
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {
    "bandit" = python.mkDerivation {
      name = "bandit-1.6.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/05/51/cbfd4b5a383d51a73a9e8cbf152037a212e0058ee8b329d4501f74cdddef/bandit-1.6.2.tar.gz";
        sha256 = "41e75315853507aa145d62a78a2a6c5e3240fe14ee7c601459d0df9418196065";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."gitpython"
        self."pyyaml"
        self."six"
        self."stevedore"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bandit.readthedocs.io/en/latest/";
        license = "UNKNOWN";
        description = "Security oriented static analyser for python code.";
      };
    };

    "gitdb2" = python.mkDerivation {
      name = "gitdb2-2.0.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c4/5c/579abccd59187eaf6b3c8a4a6ecd86fce1dfd818155bfe4c52ac28dca6b7/gitdb2-2.0.5.tar.gz";
        sha256 = "83361131a1836661a155172932a13c08bda2db3674e4caa32368aa6eb02f38c2";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."smmap2"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gitpython-developers/gitdb";
        license = licenses.bsdOriginal;
        description = "Git Object Database";
      };
    };

    "gitpython" = python.mkDerivation {
      name = "gitpython-3.0.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/51/46/993beca52f3b609d148071e129235b866626eeb6056f2faffb41d9d727a7/GitPython-3.0.2.tar.gz";
        sha256 = "d2f4945f8260f6981d724f5957bc076398ada55cb5d25aaee10108bcdc894100";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."gitdb2"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gitpython-developers/GitPython";
        license = licenses.bsdOriginal;
        description = "Python Git Library";
      };
    };

    "pbr" = python.mkDerivation {
      name = "pbr-5.4.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/99/f1/7807d3409c79905a907f1c616d910c921b2a8e73c17b2969930318f44777/pbr-5.4.3.tar.gz";
        sha256 = "2c8e420cd4ed4cec4e7999ee47409e876af575d4c35a45840d59e8b5f3155ab8";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.openstack.org/pbr/latest/";
        license = "UNKNOWN";
        description = "Python Build Reasonableness";
      };
    };

    "pyyaml" = python.mkDerivation {
      name = "pyyaml-5.1.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e3/e8/b3212641ee2718d556df0f23f78de8303f068fe29cdaa7a91018849582fe/PyYAML-5.1.2.tar.gz";
        sha256 = "01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/yaml/pyyaml";
        license = licenses.mit;
        description = "YAML parser and emitter for Python";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz";
        sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "smmap2" = python.mkDerivation {
      name = "smmap2-2.0.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/3b/ba/e49102b3e8ffff644edded25394b2d22ebe3e645f3f6a8139129c4842ffe/smmap2-2.0.5.tar.gz";
        sha256 = "29a9ffa0497e7f2be94ca0ed1ca1aa3cd4cf25a1f6b4f5f87f74b46ed91d609a";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gitpython-developers/smmap";
        license = licenses.bsdOriginal;
        description = "A pure Python implementation of a sliding window memory map manager";
      };
    };

    "stevedore" = python.mkDerivation {
      name = "stevedore-1.31.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/05/79/516aa1c427da04f818242ec147a2f417dd0e8f4abbc9302ed07459fb152d/stevedore-1.31.0.tar.gz";
        sha256 = "e0739f9739a681c7a1fda76a102b65295e96a144ccdb552f2ae03c5f0abe8a14";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pbr"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.openstack.org/stevedore/latest/";
        license = "UNKNOWN";
        description = "Manage dynamic plugins for Python applications";
      };
    };
  };
  localOverridesFile = ./bandit_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
    
  ];
  paramOverrides = [
    (overrides { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [localOverrides] else [] ) ++ commonOverrides ++ paramOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )