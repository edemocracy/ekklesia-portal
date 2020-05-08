# generated using pypi2nix tool (version: 2.0.4)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python38 -e eliot -e eliot-tree --basename eliot
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
    python = pkgs.python38;
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python38-interpreter";
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
    "boltons" = python.mkDerivation {
      name = "boltons-20.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/42/38/ce1ab39b04e1c9946a9dc1076f01d138fb0bbbda1aae48709193b30629e1/boltons-20.1.0.tar.gz";
        sha256 = "6e890b173c5f2dcb4ec62320b3799342ecb1a6a0b2253014455387665d62c213";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mahmoud/boltons";
        license = licenses.bsdOriginal;
        description = "When they're not builtins, they're boltons.";
      };
    };

    "colored" = python.mkDerivation {
      name = "colored-1.4.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b2/16/04827e24c14266d9161bd86bad50069fea453fa006c3d2b31da39251184a/colored-1.4.2.tar.gz";
        sha256 = "056fac09d9e39b34296e7618897ed1b8c274f98423770c2980d829fd670955ed";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://gitlab.com/dslackw/colored";
        license = licenses.mit;
        description = "Simple library for color and formatting to terminal";
      };
    };

    "eliot" = python.mkDerivation {
      name = "eliot-1.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/26/b5/f8fa5483623e4bda84d93ec1a5fa635470e84641d08dcf335d59724a27ce/eliot-1.12.0.tar.gz";
        sha256 = "b6e16d8a4392cac6bd07358aaef140c50059ab00fc13171012810e33e1d94b71";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."boltons"
        self."pyrsistent"
        self."six"
        self."zope-interface"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/itamarst/eliot/";
        license = licenses.asl20;
        description = "Logging library that tells you why it happened";
      };
    };

    "eliot-tree" = python.mkDerivation {
      name = "eliot-tree-19.0.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/27/2d/f63fd513883057bb05fb7a020b4f5be3874386c68d924e262e6918cde7ad/eliot-tree-19.0.1.tar.gz";
        sha256 = "aac20b528944e6e3c9d33884104f06a8de3a1840ada15d07ea036e50b58cfba1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."colored"
        self."eliot"
        self."iso8601"
        self."jmespath"
        self."six"
        self."toolz"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jonathanj/eliottree";
        license = licenses.mit;
        description = "Render Eliot logs as an ASCII tree";
      };
    };

    "iso8601" = python.mkDerivation {
      name = "iso8601-0.1.12";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/45/13/3db24895497345fb44c4248c08b16da34a9eb02643cea2754b21b5ed08b0/iso8601-0.1.12.tar.gz";
        sha256 = "49c4b20e1f38aa5cf109ddcd39647ac419f928512c869dc01d5c7098eddede82";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/micktwomey/pyiso8601";
        license = licenses.mit;
        description = "Simple module to parse ISO 8601 dates";
      };
    };

    "jmespath" = python.mkDerivation {
      name = "jmespath-0.9.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5c/40/3bed01fc17e2bb1b02633efc29878dfa25da479ad19a69cfb11d2b88ea8e/jmespath-0.9.5.tar.gz";
        sha256 = "cca55c8d153173e21baa59983015ad0daf603f9cb799904ff057bfb8ff8dc2d9";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jmespath/jmespath.py";
        license = licenses.mit;
        description = "JSON Matching Expressions";
      };
    };

    "pyrsistent" = python.mkDerivation {
      name = "pyrsistent-0.16.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/9f/0d/cbca4d0bbc5671822a59f270e4ce3f2195f8a899c97d0d5abb81b191efb5/pyrsistent-0.16.0.tar.gz";
        sha256 = "28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/tobgu/pyrsistent/";
        license = licenses.mit;
        description = "Persistent/Functional/Immutable data structures";
      };
    };

    "setuptools" = python.mkDerivation {
      name = "setuptools-46.1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b5/96/af1686ea8c1e503f4a81223d4a3410e7587fd52df03083de24161d0df7d4/setuptools-46.1.3.zip";
        sha256 = "795e0475ba6cd7fa082b1ee6e90d552209995627a2a227a47c6ea93282f4bfb1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description = "Easily download, build, install, upgrade, and uninstall Python packages";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.14.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/21/9f/b251f7f8a76dec1d6651be194dfba8fb8d7781d10ab3987190de8391d08e/six-1.14.0.tar.gz";
        sha256 = "236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "toolz" = python.mkDerivation {
      name = "toolz-0.10.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/22/8e/037b9ba5c6a5739ef0dcde60578c64d49f45f64c5e5e886531bfbc39157f/toolz-0.10.0.tar.gz";
        sha256 = "08fdd5ef7c96480ad11c12d472de21acd32359996f69a5259299b540feba4560";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytoolz/toolz/";
        license = licenses.bsdOriginal;
        description = "List processing tools and functional utilities";
      };
    };

    "zope-interface" = python.mkDerivation {
      name = "zope-interface-5.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/af/d2/9675302d7ced7ec721481f4bbecd28a390a8db4ff753d28c64057b975396/zope.interface-5.1.0.tar.gz";
        sha256 = "40e4c42bd27ed3c11b2c983fecfb03356fae1209de10686d03c02c8696a1d90e";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.interface";
        license = licenses.zpl21;
        description = "Interfaces for Python";
      };
    };
  };
  localOverridesFile = ./eliot_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
        (let src = pkgs.fetchFromGitHub { owner = "nix-community"; repo = "pypi2nix-overrides"; rev = "100c15ec7dfe7d241402ecfb1e796328d0eaf1ec"; sha256 = "0akfkvdakcdxc1lrxznh1rz2811x4pafnsq3jnyr5pn3m30pc7db"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
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