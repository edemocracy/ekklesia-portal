# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python37 -e eliot -e eliot-tree --basename eliot
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
    "boltons" = python.mkDerivation {
      name = "boltons-19.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/27/4b/ebac172f3b17bd395ea1fa1121fc85e1cd5f9dbb6d4836d2bccc44a6e333/boltons-19.1.0.tar.gz";
        sha256 = "c32b2d121331a9bc7c220050d4273f3aa359b7569cb4794188e71524603113dc";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mahmoud/boltons";
        license = licenses.bsdOriginal;
        description = "When they're not builtins, they're boltons.";
      };
    };

    "eliot" = python.mkDerivation {
      name = "eliot-1.10.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cc/c0/2489a69c5bdffdb5b784f9d1c9ece404afad1720e91a5ea5feedbbeab994/eliot-1.10.0.tar.gz";
        sha256 = "c76e22f234766be9a81eed83e636a5d77f696364adc04558722940b8761dc71e";
};
      doCheck = commonDoCheck;
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
      name = "eliot-tree-18.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e5/62/8b73c7970fcb5b8c69cf5c0aab1fe6125f498d10daa27db1d71629eb46f3/eliot-tree-18.1.1.tar.gz";
        sha256 = "d492154cbc4093faf4492dbf503e87f51e27f89c7fc8697201157e0fb8d7d027";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."eliot"
        self."iso8601"
        self."jmespath"
        self."six"
        self."termcolor"
        self."toolz"
        self."tree-format"
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/micktwomey/pyiso8601";
        license = licenses.mit;
        description = "Simple module to parse ISO 8601 dates";
      };
    };

    "jmespath" = python.mkDerivation {
      name = "jmespath-0.9.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/2c/30/f0162d3d83e398c7a3b70c91eef61d409dea205fb4dc2b47d335f429de32/jmespath-0.9.4.tar.gz";
        sha256 = "bde2aef6f44302dfb30320115b17d030798de8c4110e28d5cf6cf91a7a31074c";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jmespath/jmespath.py";
        license = licenses.mit;
        description = "JSON Matching Expressions";
      };
    };

    "pyrsistent" = python.mkDerivation {
      name = "pyrsistent-0.15.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b9/66/b2638d96a2d128b168d0dba60fdc77b7800a9b4a5340cefcc5fc4eae6295/pyrsistent-0.15.4.tar.gz";
        sha256 = "34b47fa169d6006b32e99d4b3c4031f155e6e68ebcc107d6454852e8e0ee6533";
};
      doCheck = commonDoCheck;
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

    "termcolor" = python.mkDerivation {
      name = "termcolor-1.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/8a/48/a76be51647d0eb9f10e2a4511bf3ffb8cc1e6b14e9e4fab46173aa79f981/termcolor-1.1.0.tar.gz";
        sha256 = "1d6d69ce66211143803fbc56652b41d73b4a400a2891d7bf7a1cdf4c02de613b";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/termcolor";
        license = licenses.mit;
        description = "ANSII Color formatting for output in terminal.";
      };
    };

    "toolz" = python.mkDerivation {
      name = "toolz-0.10.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/22/8e/037b9ba5c6a5739ef0dcde60578c64d49f45f64c5e5e886531bfbc39157f/toolz-0.10.0.tar.gz";
        sha256 = "08fdd5ef7c96480ad11c12d472de21acd32359996f69a5259299b540feba4560";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytoolz/toolz/";
        license = licenses.bsdOriginal;
        description = "List processing tools and functional utilities";
      };
    };

    "tree-format" = python.mkDerivation {
      name = "tree-format-0.1.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0d/91/8d860c75c3e70e6bbec7b898b5f753bf5da404be9296e245034360759645/tree-format-0.1.2.tar.gz";
        sha256 = "a538523aa78ae7a4b10003b04f3e1b37708e0e089d99c9d3b9e1c71384c9a7f9";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/jml/tree-format";
        license = "UNKNOWN";
        description = "UNKNOWN";
      };
    };

    "zope-interface" = python.mkDerivation {
      name = "zope-interface-4.6.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4e/d0/c9d16bd5b38de44a20c6dc5d5ed80a49626fafcb3db9f9efdc2a19026db6/zope.interface-4.6.0.tar.gz";
        sha256 = "1b3d0dcabc7c90b470e59e38a9acaa361be43b3a6ea644c0063951964717f0e5";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
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