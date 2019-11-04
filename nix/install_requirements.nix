# generated using pypi2nix tool (version: 2.1.0.dev1)
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
      name = "babel-2.7.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bd/78/9fb975cbb3f4b136de2cd4b5e5ce4a3341169ebf4c6c03630996d05428f1/Babel-2.7.0.tar.gz";
        sha256 = "e86135ae101e31e2c8ec20a4e0c5220f4eed12487d5cf3f78be7e98d3a57fc28";
};
      doCheck = commonDoCheck;
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
      name = "boltons-19.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/1e/70/7daff4083c31a83023b4e80d77b9b511b5b2d0885e2dd83d7aa5dccdff49/boltons-19.3.0.tar.gz";
        sha256 = "7b3344098aa0d593e1a04cd290f61310d5aefc66aeb1e07262d5afdabdb88a67";
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

    "case-conversion" = python.mkDerivation {
      name = "case-conversion-2.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cb/8c/14731e4d4f6fd9876575abc7df9861bcb0a21d764f7ac622ab5485c45afe/case_conversion-2.1.0.tar.gz";
        sha256 = "4114aaed4213f2235f1648502fd1793e5fdfa3fa86f85979fd2d0dce1584e197";
};
      doCheck = commonDoCheck;
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
      name = "certifi-2019.9.11";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/62/85/7585750fd65599e88df0fed59c74f5075d4ea2fe611deceb95dd1c2fb25b/certifi-2019.9.11.tar.gz";
        sha256 = "e4f3620cfea4f83eedc95b24abd9cd56f3c4b146dd0177e83a21b4eb49e21e50";
};
      doCheck = commonDoCheck;
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
      name = "dataclasses-json-0.3.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/45/36/8de7229fa75991b91cd4734f7f74b32e78b0244688ce8d1d02584cae874a/dataclasses-json-0.3.6.tar.gz";
        sha256 = "ebdf7407681763d6125fd00d15ed037cc3aa6f9129fe7634e8f891410e89559f";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
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
      name = "decorator-4.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dc/c3/9d378af09f5737cfd524b844cd2fbb0d2263a35c11d712043daab290144d/decorator-4.4.1.tar.gz";
        sha256 = "54c38050039232e1db4ad7375cfce6748d7b41c29e95a081c8a6d2c30364a2ce";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/micheles/decorator";
        license = licenses.bsdOriginal;
        description = "Decorators for Humans";
      };
    };

    "dectate" = python.mkDerivation {
      name = "dectate-0.13";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0d/b8/9ce9e0ee72372d4dc8817e48d26a16d63d4397424cf3b8936b6e565be4ad/dectate-0.13.tar.gz";
        sha256 = "299a5d3d674d7cd095c8489331ecece22e5a567ee8a7636e8b57bbb220c568e4";
};
      doCheck = commonDoCheck;
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

    "idna" = python.mkDerivation {
      name = "idna-2.8";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ad/13/eb56951b6f7950cadb579ca166e448ba77f9d24efc03edd7e55fa57d04b7/idna-2.8.tar.gz";
        sha256 = "c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "importscan" = python.mkDerivation {
      name = "importscan-0.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/2d/e1/01431f1afc930befc4a1e32b39e5227124ebcd5ee165683b0d8e80fdb45f/importscan-0.1.tar.gz";
        sha256 = "5c003afe8d7f48d684bc9f66e8109952234812b225be324ce572ce4278b18f10";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "UNKNOWN";
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/itsdangerous/";
        license = licenses.bsdOriginal;
        description = "Various helpers to pass data to untrusted environments and back.";
      };
    };

    "jinja2" = python.mkDerivation {
      name = "jinja2-2.10.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7b/db/1d037ccd626d05a7a47a1b81ea73775614af83c2b3e53d86a0bb41d8d799/Jinja2-2.10.3.tar.gz";
        sha256 = "9fe95f19286cfefaa917656583d020be14e7859c6b0252588391e47db34527de";
};
      doCheck = commonDoCheck;
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "marshmallow" = python.mkDerivation {
      name = "marshmallow-3.2.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d1/c1/66711e6dc7c2cb665435382636a03bed30dcc2fca12fa09500ce0059b1f8/marshmallow-3.2.1.tar.gz";
        sha256 = "9a2f3e8ea5f530a9664e882d7d04b58650f46190178b2264c72b7d20399d28f0";
};
      doCheck = commonDoCheck;
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
      name = "morepath-0.18.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/26/1c/fc413083ce6216dd459a46dea1273c57b98c2e657aeca40d5ff6487d5817/morepath-0.18.2.tar.gz";
        sha256 = "7bc289b0fe15aa74ad2faa33a6c8f3d4340395a2b8f09db1da9703d4a17bf346";
};
      doCheck = commonDoCheck;
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/oauthlib/oauthlib";
        license = licenses.bsdOriginal;
        description = "A generic, spec-compliant, thorough implementation of the OAuth request-signing logic";
      };
    };

    "passlib" = python.mkDerivation {
      name = "passlib-1.7.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/25/4b/6fbfc66aabb3017cd8c3bd97b37f769d7503ead2899bf76e570eb91270de/passlib-1.7.1.tar.gz";
        sha256 = "3d948f64138c25633613f303bcc471126eae67c04d5e3f6b7b8ce6242f8653e0";
};
      doCheck = commonDoCheck;
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
      name = "pyrsistent-0.15.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/30/86/53a88c0a57698fa228db29a4000c28f4124823010388cb7042fe6e2be8dd/pyrsistent-0.15.5.tar.gz";
        sha256 = "eb6545dbeb1aa69ab1fb4809bfbf5a8705e44d92ef8fc7c2361682a47c46c778";
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

    "pytz" = python.mkDerivation {
      name = "pytz-2019.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/c3/534ddba230bd4fbbd3b7a3d35f3341d014cca213f369a9940925e7e5f691/pytz-2019.3.tar.gz";
        sha256 = "b02c06db6cf09c12dd25137e563b31700d3b80fcc4ad23abb7a315f2789819be";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
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

    "reg" = python.mkDerivation {
      name = "reg-0.11";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/50/45/cdf15fd2fe84d9bcedc38fb42e5c0836c9e6bf21d9b0f7b40ba4cf488008/reg-0.11.tar.gz";
        sha256 = "ce61bc8c37d58477675d8eb4922ef26c1446e1691249de613f629ef286addf04";
};
      doCheck = commonDoCheck;
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
      name = "regex-2019.11.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fc/1d/13cc7d174cd2d05808abac3f5fb37433e30c4cd93b152d2a9c09c926d7e8/regex-2019.11.1.tar.gz";
        sha256 = "720e34a539a76a1fedcebe4397290604cc2bdf6f81eca44adb9fb2ea071c0c69";
};
      doCheck = commonDoCheck;
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.repoze.org";
        license = "License :: Repoze Public License";
        description = "A tiny LRU cache implementation and decorator";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.22.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/01/62/ddcf76d1d19885e8579acb1b1df26a852b03472c0e46d2b959a714c90608/requests-2.22.0.tar.gz";
        sha256 = "11e007a8a2aa0323f5a921e9e6a2d7e4e67d9877e85773fba9ba6419025cbeb4";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."chardet"
        self."idna"
        self."urllib3"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-requests.org";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
      };
    };

    "requests-oauthlib" = python.mkDerivation {
      name = "requests-oauthlib-1.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/de/a2/f55312dfe2f7a344d0d4044fdfae12ac8a24169dc668bd55f72b27090c32/requests-oauthlib-1.2.0.tar.gz";
        sha256 = "bd6533330e8748e94bf0b214775fed487d309b8b8fe823dc45641ebcd9a32f57";
};
      doCheck = commonDoCheck;
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
      name = "setuptools-41.6.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/11/0a/7f13ef5cd932a107cd4c0f3ebc9d831d9b78e1a0e8c98a098ca17b1d7d97/setuptools-41.6.0.zip";
        sha256 = "6afa61b391dcd16cb8890ec9f66cc4015a8a31a6e1c2b4e0c464514be1a3d722";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description = "Easily download, build, install, upgrade, and uninstall Python packages";
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

    "sqlalchemy" = python.mkDerivation {
      name = "sqlalchemy-1.3.10";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/14/0e/487f7fc1e432cec50d2678f94e4133f2b9e9356e35bacc30d73e8cb831fc/SQLAlchemy-1.3.10.tar.gz";
        sha256 = "0f0768b5db594517e1f5e1572c73d14cf295140756431270d89496dc13d5e46c";
};
      doCheck = commonDoCheck;
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
      name = "sqlalchemy-utils-0.35.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bf/7e/3211ad9b3983b216d1b1863fd7734f80bacd1a62a5de8ff6844fb5ed1498/SQLAlchemy-Utils-0.35.0.tar.gz";
        sha256 = "01f0f0ebed696386bc7bf9231cd6894087baba374dd60f40eb1b07512d6b1a5e";
};
      doCheck = commonDoCheck;
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/okunishinishi/python-stringcase";
        license = licenses.mit;
        description = "String case converter.";
      };
    };

    "transaction" = python.mkDerivation {
      name = "transaction-2.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/9d/7d/0e8af0d059e052b9dcf2bb5a08aad20ae3e238746bdd3f8701a60969b363/transaction-2.4.0.tar.gz";
        sha256 = "726059c461b9ec4e69e5bead6680667a3db01bf2adf901f23e4031228a0f9f9f";
};
      doCheck = commonDoCheck;
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
      name = "urllib3-1.25.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ff/44/29655168da441dff66de03952880c6e2d17b252836ff1aa4421fba556424/urllib3-1.25.6.tar.gz";
        sha256 = "9a107b99a5393caf59c7aa3c1249c16e6879447533d0887f4336dde834c7be86";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description = "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };

    "validators" = python.mkDerivation {
      name = "validators-0.14.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b2/b7/5fc43b7dba2a35362b2f5ce39dbee835c48898e2458910c3af810240fbaa/validators-0.14.0.tar.gz";
        sha256 = "f0ac832212e3ee2e9b10e156f19b106888cf1429c291fbc5297aae87685014ae";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."decorator"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/validators";
        license = licenses.bsdOriginal;
        description = "";
      };
    };

    "webob" = python.mkDerivation {
      name = "webob-1.8.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/9d/1a/0c89c070ee2829c934cb6c7082287c822e28236a4fcf90063e6be7c35532/WebOb-1.8.5.tar.gz";
        sha256 = "05aaab7975e0ee8af2026325d656e5ce14a71f1883c52276181821d6d5bf7086";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };

    "werkzeug" = python.mkDerivation {
      name = "werkzeug-0.16.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5e/fd/eb19e4f6a806cd6ee34900a687f181001c7a0059ff914752091aba84681f/Werkzeug-0.16.0.tar.gz";
        sha256 = "7280924747b5733b246fe23972186c6b348f9ae29724135a6dfc1e53cea433e7";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/werkzeug/";
        license = licenses.bsdOriginal;
        description = "The comprehensive WSGI web application library.";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.33.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/59/b0/11710a598e1e148fb7cbf9220fd2a0b82c98e94efbdecb299cb25e7f0b39/wheel-0.33.6.tar.gz";
        sha256 = "10c9da68765315ed98850f8e048347c3eb06dd81822dc2ab1d4fde9dc9702646";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python.";
      };
    };

    "zope-deprecation" = python.mkDerivation {
      name = "zope-deprecation-4.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/34/da/46e92d32d545dd067b9436279d84c339e8b16de2ca393d7b892bc1e1e9fd/zope.deprecation-4.4.0.tar.gz";
        sha256 = "0d453338f04bacf91bbfba545d8bcdf529aa829e67b705eac8c1a7fdce66e2df";
};
      doCheck = commonDoCheck;
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
      name = "zope-interface-4.6.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4e/d0/c9d16bd5b38de44a20c6dc5d5ed80a49626fafcb3db9f9efdc2a19026db6/zope.interface-4.6.0.tar.gz";
        sha256 = "1b3d0dcabc7c90b470e59e38a9acaa361be43b3a6ea644c0063951964717f0e5";
};
      doCheck = commonDoCheck;
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
      name = "zope-sqlalchemy-1.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bd/f7/01e671797b619002b90a12faee782328ee60768884c717215ec3153a7228/zope.sqlalchemy-1.2.tar.gz";
        sha256 = "069eaad5a15f187603f368a10e0e6b0d485663498c2fe2f8ac7e93f810326eeb";
};
      doCheck = commonDoCheck;
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
        (let src = pkgs.fetchFromGitHub { owner = "nix-community"; repo = "pypi2nix-overrides"; rev = "9c4599dc3ee95cb2e56278d8ea4ceb33de0e8d23"; sha256 = "0hgnmylwq13hi0gqwcjy1q72n747g5sc2wz5bys41asrrpxqwaw3"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
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