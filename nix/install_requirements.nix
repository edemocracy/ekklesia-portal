# generated using pypi2nix tool (version: 2.0.4)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python37 -r ../python_requirements/install_requirements.txt --basename install_requirements -E postgresql_11 -E libffi -E openssl.dev
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

  commonBuildInputs = with pkgs; [ postgresql_11 libffi openssl.dev ];
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
    "attrs" = python.mkDerivation {
      name = "attrs-19.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/98/c3/2c227e66b5e896e15ccdae2e00bbc69aa46e9a8ce8869cc5fa96310bf612/attrs-19.3.0.tar.gz";
        sha256 = "f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "babel" = python.mkDerivation {
      name = "babel-2.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/34/18/8706cfa5b2c73f5a549fdc0ef2e24db71812a2685959cff31cbdfc010136/Babel-2.8.0.tar.gz";
        sha256 = "1aac2ae2d0d8ea368fa90906567f5c08463d98ade155c0c4bfedd6a0f7160e38";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytz"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://babel.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "Internationalization utilities";
      };
    };

    "boltons" = python.mkDerivation {
      name = "boltons-20.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/8e/9a/68d04e4b02b802ac20a47e5bf4731bea79b9e6ee9efc5adae5228136823c/boltons-20.0.0.tar.gz";
        sha256 = "e44ddbd10af0904147c194d2c9bd2affa6a3e5b2ebfb9d5547900d8931203953";
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

    "cachetools" = python.mkDerivation {
      name = "cachetools-4.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ff/e9/879bc23137b5c19f93c2133a6063874b83c8e1912ff1467a3d4331598921/cachetools-4.0.0.tar.gz";
        sha256 = "9a52dd97a85f257f4e4127f15818e71a0c7899f121b34591fcc1173ea79a0198";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tkem/cachetools/";
        license = licenses.mit;
        description = "Extensible memoizing collections and decorators";
      };
    };

    "case-conversion" = python.mkDerivation {
      name = "case-conversion-2.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cb/8c/14731e4d4f6fd9876575abc7df9861bcb0a21d764f7ac622ab5485c45afe/case_conversion-2.1.0.tar.gz";
        sha256 = "4114aaed4213f2235f1648502fd1793e5fdfa3fa86f85979fd2d0dce1584e197";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."regex"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/AlejandroFrias/case-conversion";
        license = licenses.mit;
        description = "Convert between different types of cases (unicode supported)";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2019.11.28";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/41/bf/9d214a5af07debc6acf7f3f257265618f1db242a3f8e49a9b516f24523a6/certifi-2019.11.28.tar.gz";
        sha256 = "25b64c7da4cd7479594d035c08c2d809eb4aab3a26e5a990ea98cc450c320f1f";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };

    "chameleon" = python.mkDerivation {
      name = "chameleon-3.6.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/9e/12/ad477cf8fef73154d78081575d5c8be8d3ce25e5bfe55c63e14dcb793822/Chameleon-3.6.2.tar.gz";
        sha256 = "9a9e5e068ee323817705a793cc03538677915c3b99c3f8a4ecba42e62d66862b";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://chameleon.readthedocs.io";
        license = "BSD-like (http://repoze.org/license.html)";
        description = "Fast HTML/XML Template Compiler.";
      };
    };

    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz";
        sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "colander" = python.mkDerivation {
      name = "colander-1.7.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/db/e4/74ab06f54211917b41865cafc987ce511e35503de48da9bfe9358a1bdc3e/colander-1.7.0.tar.gz";
        sha256 = "d758163a22d22c39b9eaae049749a5cd503f341231a02ed95af480b1145e81f2";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."iso8601"
        self."translationstring"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pylonsproject.org/projects/colander/en/latest/";
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
        description = "A simple schema-based serialization and deserialization library";
      };
    };

    "dataclasses-json" = python.mkDerivation {
      name = "dataclasses-json-0.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/8e/c103e8762775d2b4453119271c4e5629b445b9686a15069be548950e3ca4/dataclasses-json-0.4.1.tar.gz";
        sha256 = "2d20a1deb0745b5976174d1a7c397771a84a081abda9deed9619fcdba82c332d";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."cachetools"
        self."marshmallow"
        self."marshmallow-enum"
        self."stringcase"
        self."typing-inspect"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/lidatong/dataclasses-json";
        license = licenses.mit;
        description = "Easily serialize dataclasses to and from JSON";
      };
    };

    "decorator" = python.mkDerivation {
      name = "decorator-4.4.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/da/93/84fa12f2dc341f8cf5f022ee09e109961055749df2d0c75c5f98746cfe6c/decorator-4.4.2.tar.gz";
        sha256 = "e3a62f0520172440ca0dcc823749319382e377f37f140a0b99ef45fecb84bfe7";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/micheles/decorator";
        license = licenses.bsdOriginal;
        description = "Decorators for Humans";
      };
    };

    "dectate" = python.mkDerivation {
      name = "dectate-0.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/67/3c/86eb41eac065a1148b00fb9c9e5c4d5ebf765121499c687c6f2ec8adf07b/dectate-0.14.tar.gz";
        sha256 = "56213abfe6ce31d6fe10dbf7a7cd94e07a26d5dc7cd0ae2e208c4ef2dbebb504";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://dectate.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A configuration engine for Python frameworks";
      };
    };

    "deform" = python.mkDerivation {
      name = "deform-2.0.8";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/21/d0/45fdf891a82722c02fc2da319cf2d1ae6b5abf9e470ad3762135a895a868/deform-2.0.8.tar.gz";
        sha256 = "8936b70c622406eb8c8259c88841f19eb2996dffcf2bac123126ada851da7271";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."chameleon"
        self."colander"
        self."iso8601"
        self."peppercorn"
        self."translationstring"
        self."zope-deprecation"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pylonsproject.org/projects/deform/en/latest/";
        license = "License :: Repoze Public License";
        description = "Form library with advanced features like nested forms";
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

    "idna" = python.mkDerivation {
      name = "idna-2.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cb/19/57503b5de719ee45e83472f339f617b0c01ad75cba44aba1e4c97c2b0abd/idna-2.9.tar.gz";
        sha256 = "7588d1c14ae4c77d74036e8c22ff447b26d0fde8f007354fd48a7814db15b7cb";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "importscan" = python.mkDerivation {
      name = "importscan-0.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/18/21/3a81623fc43ca4d476c0414729948bcb790059cd35b170612b2da534e94a/importscan-0.2.tar.gz";
        sha256 = "4fb19627e1349dfd7d49d9bbd1b1bfff0f0a13e884d6cf9dcaf16f865375c9b2";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://importscan.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Recursively import modules and sub-packages";
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

    "itsdangerous" = python.mkDerivation {
      name = "itsdangerous-1.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/68/1a/f27de07a8a304ad5fa817bbe383d1238ac4396da447fa11ed937039fa04b/itsdangerous-1.1.0.tar.gz";
        sha256 = "321b033d07f2a4136d3ec762eac9f16a10ccd60f53c0c91af90217ace7ba1f19";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/itsdangerous/";
        license = licenses.bsdOriginal;
        description = "Various helpers to pass data to untrusted environments and back.";
      };
    };

    "jinja2" = python.mkDerivation {
      name = "jinja2-2.11.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d8/03/e491f423379ea14bb3a02a5238507f7d446de639b623187bccc111fbecdf/Jinja2-2.11.1.tar.gz";
        sha256 = "93187ffbc7808079673ef52771baa950426fd664d3aad1d0fa3e95644360e250";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."markupsafe"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/jinja/";
        license = licenses.bsdOriginal;
        description = "A very fast and expressive template engine.";
      };
    };

    "markdown" = python.mkDerivation {
      name = "markdown-2.6.11";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b3/73/fc5c850f44af5889192dff783b7b0d8f3fe8d30b65c8e3f78f8f0265fecf/Markdown-2.6.11.tar.gz";
        sha256 = "a856869c7ff079ad84a3e19cd87a64998350c2b94e9e08e44270faef33400f81";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://Python-Markdown.github.io/";
        license = licenses.bsdOriginal;
        description = "Python implementation of Markdown.";
      };
    };

    "markupsafe" = python.mkDerivation {
      name = "markupsafe-1.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094/MarkupSafe-1.1.1.tar.gz";
        sha256 = "29872e92839765e546828bb7754a68c418d927cd064fd4708fab9fe9c8bb116b";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "marshmallow" = python.mkDerivation {
      name = "marshmallow-3.5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a8/74/5aa84008ddc6e8fee93d961a9f04a745a349ad197d95ab89723c097b330d/marshmallow-3.5.1.tar.gz";
        sha256 = "90854221bbb1498d003a0c3cc9d8390259137551917961c8b5258c64026b2f85";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/marshmallow-code/marshmallow";
        license = licenses.mit;
        description = "A lightweight library for converting complex datatypes to and from native Python datatypes.";
      };
    };

    "marshmallow-enum" = python.mkDerivation {
      name = "marshmallow-enum-1.5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/8e/8c/ceecdce57dfd37913143087fffd15f38562a94f0d22823e3c66eac0dca31/marshmallow-enum-1.5.1.tar.gz";
        sha256 = "38e697e11f45a8e64b4a1e664000897c659b60aa57bfa18d44e226a9920b6e58";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."marshmallow"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "UNKNOWN";
        license = licenses.mit;
        description = "Enum field for Marshmallow";
      };
    };

    "more-babel-i18n" = python.mkDerivation {
      name = "more-babel-i18n-19.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0f/9c/36481507a50f28cb71f4e8279dca0df2b93eb12e09e4751cd7829a2845a8/more.babel_i18n-19.8.0.tar.gz";
        sha256 = "8b0cd6e7a7edf9ba46cb3412b7ae8ba305944de67e957a289bcfd76858d150ab";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."babel"
        self."jinja2"
        self."morepath"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/dpausp/more.babel_i18n";
        license = licenses.bsdOriginal;
        description = "i18n/l10n support for Morepath applications and Jinja2 templates";
      };
    };

    "more-browser-session" = python.mkDerivation {
      name = "more-browser-session-19.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a0/e8/d9588492ffe4a8541daecac1454cbbb58d00fb0ecaca272e7c4a10d94c46/more.browser_session-19.8.0.tar.gz";
        sha256 = "80ebd95865a1270687d5bbb9f2dc3b6e7fe27f06a2711515278b74b534cfef55";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."itsdangerous"
        self."morepath"
        self."werkzeug"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/dpausp/more.browser_session";
        license = licenses.bsdOriginal;
        description = "Session support for Morepath applications";
      };
    };

    "more-forwarded" = python.mkDerivation {
      name = "more-forwarded-0.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7c/d8/e14f30346a9da2dc705f2206a04c70d40dc03e8238f3a9ac4bb668aedb25/more.forwarded-0.2.tar.gz";
        sha256 = "d6e89b4990dc98fe4476d1dea3c49506a3434d5fc8118d48afaeecfcaa0595c3";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."morepath"
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/more.static";
        license = licenses.bsdOriginal;
        description = "Forwarded header support for Morepath";
      };
    };

    "more-itsdangerous" = python.mkDerivation {
      name = "more-itsdangerous-0.0.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/56/22/a423e8d148b628cf62f8bc8ec63ffdbda62258783e68c743c987321e68f0/more.itsdangerous-0.0.2.tar.gz";
        sha256 = "c0352ec418cb5f356261d88c600c18f7d7627895d357fe2f933fe643e42ba0f2";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."itsdangerous"
        self."morepath"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/morepath/more.itsdangerous";
        license = licenses.bsdOriginal;
        description = "An identity policy for morepath using itsdangerous.";
      };
    };

    "more-transaction" = python.mkDerivation {
      name = "more-transaction-0.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/16/fa/764e2a21bf42a3f15f07144548ae00503a982b94f81f845732e090ffd652/more.transaction-0.9.tar.gz";
        sha256 = "b5ce7d11e6c71bb3b8b6eee060d25433e4ff7c377b5d42693d0be14a7a856ce6";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."morepath"
        self."setuptools"
        self."transaction"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/morepath/more.transaction";
        license = licenses.bsdOriginal;
        description = "transaction integration for Morepath";
      };
    };

    "morepath" = python.mkDerivation {
      name = "morepath-0.19";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fd/e0/d8c1a4ac30fa6e491d8340e793fd770609ca7384a0ec32291ebb68698fb4/morepath-0.19.tar.gz";
        sha256 = "3d3f075083766e7d9c1bd184bf927590e862caa8a385f9a8a572422c0d69606a";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."dectate"
        self."importscan"
        self."reg"
        self."setuptools"
        self."webob"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://morepath.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A micro web-framework with superpowers";
      };
    };

    "munch" = python.mkDerivation {
      name = "munch-2.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/43/a1/ec48010724eedfe2add68eb7592a0d238590e14e08b95a4ffb3c7b2f0808/munch-2.5.0.tar.gz";
        sha256 = "2d735f6f24d4dba3417fa448cae40c6e896ec1fdab6cdb5e6510999758a4dbd2";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/Infinidat/munch";
        license = licenses.mit;
        description = "A dot-accessible dictionary (a la JavaScript objects)";
      };
    };

    "mypy-extensions" = python.mkDerivation {
      name = "mypy-extensions-0.4.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/63/60/0582ce2eaced55f65a4406fc97beba256de4b7a95a0034c6576458c6519f/mypy_extensions-0.4.3.tar.gz";
        sha256 = "2d82818f5bb3e369420cb3c4060a7970edba416647068eb4c5343488a6c604a8";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/python/mypy_extensions";
        license = licenses.mit;
        description = "Experimental type system extensions for programs checked with the mypy typechecker.";
      };
    };

    "oauthlib" = python.mkDerivation {
      name = "oauthlib-3.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fc/c7/829c73c64d3749da7811c06319458e47f3461944da9d98bb4df1cb1598c2/oauthlib-3.1.0.tar.gz";
        sha256 = "bee41cc35fcca6e988463cacc3bcb8a96224f470ca547e697b604cc697b2f889";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/oauthlib/oauthlib";
        license = licenses.bsdOriginal;
        description = "A generic, spec-compliant, thorough implementation of the OAuth request-signing logic";
      };
    };

    "passlib" = python.mkDerivation {
      name = "passlib-1.7.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6d/6b/4bfca0c13506535289b58f9c9761d20f56ed89439bfe6b8e07416ce58ee1/passlib-1.7.2.tar.gz";
        sha256 = "8d666cef936198bc2ab47ee9b0410c94adf2ba798e5a84bf220be079ae7ab6a8";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ecollins/passlib";
        license = licenses.bsdOriginal;
        description = "comprehensive password hashing framework supporting over 30 schemes";
      };
    };

    "peppercorn" = python.mkDerivation {
      name = "peppercorn-0.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e4/77/93085de7108cdf1a0b092ff443872a8f9442c736d7ddebdf2f27627935f4/peppercorn-0.6.tar.gz";
        sha256 = "96d7681d7a04545cfbaf2c6fb66de67b29cfc42421aa263e4c78f2cbb85be4c6";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pylonsproject.org/projects/peppercorn/en/latest/";
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
        description = "A library for converting a token stream into a data structure for use in web form posts";
      };
    };

    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.8.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/84/d7/6a93c99b5ba4d4d22daa3928b983cec66df4536ca50b22ce5dcac65e4e71/psycopg2-2.8.4.tar.gz";
        sha256 = "f898e5cc0a662a9e12bde6f931263a1bbd350cfb18e1d5336a12927851825bb6";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };

    "py-gfm" = python.mkDerivation {
      name = "py-gfm-0.1.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/06/ee/004a03a1d92bb386dae44f6dd087db541bc5093374f1637d4d4ae5596cc2/py-gfm-0.1.4.tar.gz";
        sha256 = "ef6750c579d26651cfd23968258b604228fd71b2a4e1f71dea3bea289e01377e";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."markdown"
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopieux/py-gfm";
        license = licenses.bsdOriginal;
        description = "An implementation of Github-Flavored Markdown written as an extension to the Python Markdown library.";
      };
    };

    "pyjade" = python.mkDerivation {
      name = "pyjade-4.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4a/04/396ec24e806fd3af7ea5d0f3cb6c7bbd4d00f7064712e4dd48f24c02ca95/pyjade-4.0.0.tar.gz";
        sha256 = "8d95b741de09c4942259fc3d1ad7b4f48166e69cef6f11c172e4b2c458b1ccd7";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/syrusakbary/pyjade";
        license = licenses.mit;
        description = "Jade syntax template adapter for Django, Jinja2, Mako and Tornado templates";
      };
    };

    "pyrsistent" = python.mkDerivation {
      name = "pyrsistent-0.15.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/90/aa/cdcf7ef88cc0f831b6f14c8c57318824c9de9913fe8de38e46a98c069a35/pyrsistent-0.15.7.tar.gz";
        sha256 = "cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280";
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

    "pytz" = python.mkDerivation {
      name = "pytz-2019.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/c3/534ddba230bd4fbbd3b7a3d35f3341d014cca213f369a9940925e7e5f691/pytz-2019.3.tar.gz";
        sha256 = "b02c06db6cf09c12dd25137e563b31700d3b80fcc4ad23abb7a315f2789819be";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
      };
    };

    "pyyaml" = python.mkDerivation {
      name = "pyyaml-5.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/3d/d9/ea9816aea31beeadccd03f1f8b625ecf8f645bd66744484d162d84803ce5/PyYAML-5.3.tar.gz";
        sha256 = "e9f45bd5b92c7974e59bcd2dcc8631a6b6cc380a904725fce7bc08872e691615";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/yaml/pyyaml";
        license = licenses.mit;
        description = "YAML parser and emitter for Python";
      };
    };

    "reg" = python.mkDerivation {
      name = "reg-0.12";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/84/f7/35426ebde7d795998a086932d418fe0cafcf512d2e799c97a9de55e1e351/reg-0.12.tar.gz";
        sha256 = "e614db46d661d3967657b365fc82aba5f4cd7540d8d81a5fc77dc5adfb5e79f4";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."repoze-lru"
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://reg.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Clever dispatch";
      };
    };

    "regex" = python.mkDerivation {
      name = "regex-2020.2.20";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e8/76/8ac7f467617b9cfbafcef3c76df6f22b15de654a62bea719792b00a83195/regex-2020.2.20.tar.gz";
        sha256 = "9e9624440d754733eddbcd4614378c18713d2d9d0dc647cf9c72f64e39671be5";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/mrabarnett/mrab-regex";
        license = licenses.psfl;
        description = "Alternative regular expression module, to replace re.";
      };
    };

    "repoze-lru" = python.mkDerivation {
      name = "repoze-lru-0.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/12/bc/595a77c4b5e204847fdf19268314ef59c85193a9dc9f83630fc459c0fee5/repoze.lru-0.7.tar.gz";
        sha256 = "0429a75e19380e4ed50c0694e26ac8819b4ea7851ee1fc7583c8572db80aff77";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.repoze.org";
        license = "License :: Repoze Public License";
        description = "A tiny LRU cache implementation and decorator";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.23.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f5/4f/280162d4bd4d8aad241a21aecff7a6e46891b905a4341e7ab549ebaf7915/requests-2.23.0.tar.gz";
        sha256 = "b3f43d496c6daba4493e7c431722aeb7dbc6288f52a6e04e7b6023b0247817e6";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."chardet"
        self."idna"
        self."urllib3"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://requests.readthedocs.io";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
      };
    };

    "requests-oauthlib" = python.mkDerivation {
      name = "requests-oauthlib-1.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/23/eb/68fc8fa86e0f5789832f275c8289257d8dc44dbe93fce7ff819112b9df8f/requests-oauthlib-1.3.0.tar.gz";
        sha256 = "b4261601a71fd721a8bd6d7aa1cc1d6a8a93b4a9f5e96626f8e4d91e8beeaa6a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."oauthlib"
        self."requests"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/requests/requests-oauthlib";
        license = licenses.bsdOriginal;
        description = "OAuthlib authentication support for Requests.";
      };
    };

    "setuptools" = python.mkDerivation {
      name = "setuptools-46.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/df/ed/bea598a87a8f7e21ac5bbf464102077c7102557c07db9ff4e207bd9f7806/setuptools-46.0.0.zip";
        sha256 = "2f00f25b780fbfd0787e46891dcccd805b08d007621f24629025f48afef444b5";
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

    "sqlalchemy" = python.mkDerivation {
      name = "sqlalchemy-1.3.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f5/d8/3cc1c814b29c6ac667200e19e9cf1879479f6ad561595fa313bcd99f3e0f/SQLAlchemy-1.3.14.tar.gz";
        sha256 = "b92d2de62e43499d85b1780274d1b562e5159c7996f6f04a9bb46cf681ced45f";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.sqlalchemy.org";
        license = licenses.mit;
        description = "Database Abstraction Library";
      };
    };

    "sqlalchemy-searchable" = python.mkDerivation {
      name = "sqlalchemy-searchable-1.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/93/6e/9df05493d1bbc96eb1ca2c7ab87879a299399c9aa4ea73af52c159824884/SQLAlchemy-Searchable-1.1.0.tar.gz";
        sha256 = "b48e67ef238a154e4b8de84637ef9645c213a2367b1f1915dd2f65242b2f04b2";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."sqlalchemy"
        self."sqlalchemy-utils"
        self."validators"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-searchable";
        license = licenses.bsdOriginal;
        description = "Provides fulltext search capabilities for declarative SQLAlchemy models.";
      };
    };

    "sqlalchemy-utils" = python.mkDerivation {
      name = "sqlalchemy-utils-0.36.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/85/d8/e889f8071c17773ca0ea3a67a4897ca008e7aff4e5bde0e5b9ef1ee29f1f/SQLAlchemy-Utils-0.36.1.tar.gz";
        sha256 = "4e637c88bf3ac5f99b7d72342092a1f636bea1287b2e3e17d441b0413771f86e";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
        self."sqlalchemy"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-utils";
        license = licenses.bsdOriginal;
        description = "Various utility functions for SQLAlchemy.";
      };
    };

    "stringcase" = python.mkDerivation {
      name = "stringcase-1.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f3/1f/1241aa3d66e8dc1612427b17885f5fcd9c9ee3079fc0d28e9a3aeeb36fa3/stringcase-1.2.0.tar.gz";
        sha256 = "48a06980661908efe8d9d34eab2b6c13aefa2163b3ced26972902e3bdfd87008";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/okunishinishi/python-stringcase";
        license = licenses.mit;
        description = "String case converter.";
      };
    };

    "transaction" = python.mkDerivation {
      name = "transaction-3.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4d/9a/f7c715eba8488e5b8ec0030aecd3065a7cfaf7b0a3fe6a466ec9d384c8d1/transaction-3.0.0.tar.gz";
        sha256 = "3b0ad400cb7fa25f95d1516756c4c4557bb78890510f69393ad0bd15869eaa2d";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."zope-interface"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/transaction";
        license = licenses.zpl21;
        description = "Transaction management for Python";
      };
    };

    "translationstring" = python.mkDerivation {
      name = "translationstring-1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5e/eb/bee578cc150b44c653b63f5ebe258b5d0d812ddac12497e5f80fcad5d0b4/translationstring-1.3.tar.gz";
        sha256 = "4ee44cfa58c52ade8910ea0ebc3d2d84bdcad9fa0422405b1801ec9b9a65b72d";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pylonsproject.org";
        license = "BSD-like (http://repoze.org/license.html)";
        description = "Utility library for i18n relied on by various Repoze and Pyramid packages";
      };
    };

    "typing-extensions" = python.mkDerivation {
      name = "typing-extensions-3.7.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e7/dd/f1713bc6638cc3a6a23735eff6ee09393b44b96176d3296693ada272a80b/typing_extensions-3.7.4.1.tar.gz";
        sha256 = "091ecc894d5e908ac75209f10d5b4f118fbdb2eb1ede6a63544054bb1edb41f2";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/python/typing/blob/master/typing_extensions/README.rst";
        license = licenses.psfl;
        description = "Backported and Experimental Type Hints for Python 3.5+";
      };
    };

    "typing-inspect" = python.mkDerivation {
      name = "typing-inspect-0.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d6/d2/3c8d0a885995ee81e0a52dca5093d0c3dccf511a009944e62d4ab14c9c2f/typing_inspect-0.5.0.tar.gz";
        sha256 = "811b44f92e780b90cfe7bac94249a4fae87cfaa9b40312765489255045231d9c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."mypy-extensions"
        self."typing-extensions"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/ilevkivskyi/typing_inspect";
        license = licenses.mit;
        description = "Runtime inspection utilities for typing module.";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.25.8";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/09/06/3bc5b100fe7e878d3dee8f807a4febff1a40c213d2783e3246edde1f3419/urllib3-1.25.8.tar.gz";
        sha256 = "87716c2d2a7121198ebcb7ce7cccf6ce5e9ba539041cfbaeecfb641dc0bf6acc";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description = "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };

    "validators" = python.mkDerivation {
      name = "validators-0.14.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4d/56/9b48c918ef118ea12b90f227c4498ed4703b418bdd8fb49479dfcbeae4ef/validators-0.14.2.tar.gz";
        sha256 = "b192e6bde7d617811d59f50584ed240b580375648cd032d106edeb3164099508";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."decorator"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/validators";
        license = licenses.mit;
        description = "";
      };
    };

    "webob" = python.mkDerivation {
      name = "webob-1.8.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/2a/32/5f3f43d0784bdd9392db0cb98434d7cd23a0d8a420c4d243ad4cb8517f2a/WebOb-1.8.6.tar.gz";
        sha256 = "aa3a917ed752ba3e0b242234b2a373f9c4e2a75d35291dcbe977649bd21fd108";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };

    "werkzeug" = python.mkDerivation {
      name = "werkzeug-1.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4b/a5/781dbff5062f31e8407242ea2e07c05eb4f3a236f59124ef46f5e92a2776/Werkzeug-1.0.0.tar.gz";
        sha256 = "169ba8a33788476292d04186ab33b01d6add475033dfc07215e6d219cc077096";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/werkzeug/";
        license = licenses.bsdOriginal;
        description = "The comprehensive WSGI web application library.";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.34.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/75/28/521c6dc7fef23a68368efefdcd682f5b3d1d58c2b90b06dc1d0b805b51ae/wheel-0.34.2.tar.gz";
        sha256 = "8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python";
      };
    };

    "zope-deprecation" = python.mkDerivation {
      name = "zope-deprecation-4.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/34/da/46e92d32d545dd067b9436279d84c339e8b16de2ca393d7b892bc1e1e9fd/zope.deprecation-4.4.0.tar.gz";
        sha256 = "0d453338f04bacf91bbfba545d8bcdf529aa829e67b705eac8c1a7fdce66e2df";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.deprecation";
        license = licenses.zpl21;
        description = "Zope Deprecation Infrastructure";
      };
    };

    "zope-interface" = python.mkDerivation {
      name = "zope-interface-4.7.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f8/44/8531e65de6fde76e6055f5ce93e8a482dff534cea9bebcac7845e2273efd/zope.interface-4.7.2.tar.gz";
        sha256 = "fd1101bd3fcb4f4cf3485bb20d6cb0b56909b94d3bd2a53a6cb9d381c3da3365";
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

    "zope-sqlalchemy" = python.mkDerivation {
      name = "zope-sqlalchemy-1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ba/1d/4ddb68ab3661c330b41a2b24f9c806b51e9f66cac5382c608f476bd5403b/zope.sqlalchemy-1.3.tar.gz";
        sha256 = "b9c689d39d83856b5a81ac45dbd3317762bf6a2b576c5dd13aaa2c56e0168154";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
        self."sqlalchemy"
        self."transaction"
        self."zope-interface"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.sqlalchemy";
        license = licenses.zpl21;
        description = "Minimal Zope/SQLAlchemy transaction integration";
      };
    };
  };
  localOverridesFile = ./install_requirements_override.nix;
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