# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V 3.7 -r frozen_install_requirements.txt -E postgresql -E libffi --basename install_requirements
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
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            if [ -e $out/${pkgs.python37.sitePackages}/pip/req/req_install.py ]; then
              sed -i \
                -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"  \
                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"  \
                $out/${pkgs.python37.sitePackages}/pip/req/req_install.py
            fi
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql libffi ];
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
      name = "attrs-19.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cc/d9/931a24cc5394f19383fbbe3e1147a0291276afa43a0dc3ed0d6cd9fda813/attrs-19.1.0.tar.gz";
        sha256 = "f0b870f674851ecbfbbbd364d6b5cbdff9dcedbc7f3f5e18a6891057f21fe399";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
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
      name = "certifi-2019.6.16";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c5/67/5d0548226bcc34468e23a0333978f0e23d28d0b3f0c71a151aef9c3f7680/certifi-2019.6.16.tar.gz";
        sha256 = "945e3ba63a0b9f577b1395204e13c3a231f9bc0223888be653286534e5873695";
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
        license = licenses.lgpl3;
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
      buildInputs = commonBuildInputs ++ [ ];
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
      name = "dataclasses-json-0.2.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/16/6a/dc8a9587c6297f715ab915bc8e84814cdcdb4463b841a6b767aa7113b26d/dataclasses-json-0.2.14.tar.gz";
        sha256 = "16fdc36ec471fb6cc2054ff5ce2be78876d16f78cee6be3e49137c7fcf31667f";
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
      name = "decorator-4.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ba/19/1119fe7b1e49b9c8a9f154c930060f37074ea2e8f9f6558efc2eeaa417a2/decorator-4.4.0.tar.gz";
        sha256 = "86156361c50488b84a3f148056ea716ca587df2f0de1d34750d35c21312725de";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/micheles/decorator";
        license = "new BSD License";
        description = "Better living through Python with decorators";
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
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://dectate.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A configuration engine for Python frameworks";
      };
    };

    "deform" = python.mkDerivation {
      name = "deform-2.0.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cf/a1/bc234527b8f181de9acd80e796483c00007658d1e32b7de78f1c2e004d9a/deform-2.0.7.tar.gz";
        sha256 = "2ff29c32ebe544c0f0a77087e268b2cd9cb4b11fa35af3635d5b42913f88d74a";
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
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
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
      propagatedBuildInputs = [ ];
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
      name = "jinja2-2.10.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/93/ea/d884a06f8c7f9b7afbc8138b762e80479fb17aedbbe2b06515a12de9378d/Jinja2-2.10.1.tar.gz";
        sha256 = "065c4f02ebe7f7cf559e49ee5a95fb800a9e4528727aec6f24402a5374c65013";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."babel"
        self."markupsafe"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://jinja.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "A small but fast and easy to use stand-alone template engine written in pure python.";
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
        license = licenses.bsd3;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "marshmallow" = python.mkDerivation {
      name = "marshmallow-3.0.0rc6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/91/0d/c91fc9cbc7e737ddc01d5b55900d7611ea52bd24c0660ea2e4df1a3e0ac9/marshmallow-3.0.0rc6.tar.gz";
        sha256 = "8c6a22cfc9ca33945e2707c771c44030a035be96082a18643d431280b9b8f08e";
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
        self."webob"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://morepath.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A micro web-framework with superpowers";
      };
    };

    "munch" = python.mkDerivation {
      name = "munch-2.3.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/68/f4/260ec98ea840757a0da09e0ed8135333d59b8dfebe9752a365b04857660a/munch-2.3.2.tar.gz";
        sha256 = "6ae3d26b837feacf732fb8aa5b842130da1daf221f5af9f9d4b2a0a6414b0d51";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/Infinidat/munch";
        license = licenses.mit;
        description = "A dot-accessible dictionary (a la JavaScript objects).";
      };
    };

    "mypy-extensions" = python.mkDerivation {
      name = "mypy-extensions-0.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c2/92/3cc05d1206237d54db7b2565a58080a909445330b4f90a6436302a49f0f8/mypy_extensions-0.4.1.tar.gz";
        sha256 = "37e0e956f41369209a3d5f34580150bcacfabaa57b33a15c0b25f4b5725e0812";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.mypy-lang.org/";
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
      name = "psycopg2-2.8.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5c/1c/6997288da181277a0c29bc39a5f9143ff20b8c99f2a7d059cfb55163e165/psycopg2-2.8.3.tar.gz";
        sha256 = "897a6e838319b4bf648a574afb6cabcb17d0488f8c7195100d48d872419f4457";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.zpl21;
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
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopieux/py-gfm";
        license = "UNKNOWN";
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

    "pytz" = python.mkDerivation {
      name = "pytz-2019.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/27/c0/fbd352ca76050952a03db776d241959d5a2ee1abddfeb9e2a53fdb489be4/pytz-2019.2.tar.gz";
        sha256 = "26c0b32e437e54a18161324a2fca3c4b9846b74a8dccddd843113109e1116b32";
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
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://reg.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Clever dispatch";
      };
    };

    "regex" = python.mkDerivation {
      name = "regex-2019.8.19";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6f/a6/99eeb5904ab763db87af4bd71d9b1dfdd9792681240657a4c0a599c10a81/regex-2019.08.19.tar.gz";
        sha256 = "587b62d48ca359d2d4f02d486f1f0aa9a20fbaf23a9d4198c4bed72ab2f6c849";
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
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
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
        license = "ISC";
        description = "OAuthlib authentication support for Requests.";
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
      name = "sqlalchemy-1.3.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c2/75/6217c626fa22ad56ae5ccb1a36e7c4f17f5ca31543887e00179468d10464/SQLAlchemy-1.3.7.tar.gz";
        sha256 = "0459bf0ea6478f3e904de074d65769a11d74cdc34438ab3159250c96d089aef0";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."psycopg2"
      ];
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
      name = "sqlalchemy-utils-0.34.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/45/61/3bdd2931e86253fa7df6445a26929fbcc9bc43ad6b27a10f991eb6ecde75/SQLAlchemy-Utils-0.34.2.tar.gz";
        sha256 = "6689b29d7951c5c7c4d79fa6b8c95f9ff9ec708b07aa53f82060599bd14dcc88";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."babel"
        self."jinja2"
        self."passlib"
        self."psycopg2"
        self."pytz"
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

    "typing-inspect" = python.mkDerivation {
      name = "typing-inspect-0.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ae/6c/0f91f0d13be6a6ceba8605315fd29f1ea97f1e6556c52199eb9f3d70f0bd/typing_inspect-0.4.0.tar.gz";
        sha256 = "cf41eb276cc8955a45e03c15cd1efa6c181a8775a38ff0bfda99d28af97bcda3";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."mypy-extensions"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/ilevkivskyi/typing_inspect";
        license = licenses.mit;
        description = "Runtime inspection utilities for typing module.";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.25.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4c/13/2386233f7ee40aa8444b47f7463338f3cbdf00c316627558784e3f542f07/urllib3-1.25.3.tar.gz";
        sha256 = "dbe59173209418ae49d485b87d1681aefa36252ee85884c31346debd19463232";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."idna"
      ];
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
      name = "werkzeug-0.15.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c7/fb/56734c47bc5bb4d00898c2581bc08166cb6fea72b6894cf279053521c25a/Werkzeug-0.15.5.tar.gz";
        sha256 = "a13b74dd3c45f758d4ebdb224be8f1ab8ef58b3c0ffc1783a8c7d9f4f50227e6";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/werkzeug/";
        license = licenses.bsd3;
        description = "The comprehensive WSGI web application library.";
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
      propagatedBuildInputs = [ ];
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
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.interface";
        license = licenses.zpl21;
        description = "Interfaces for Python";
      };
    };

    "zope-sqlalchemy" = python.mkDerivation {
      name = "zope-sqlalchemy-1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b8/4f/4a372512cd37885c572dc7d36d3befe8adecb07e451d1f03723b29c947f2/zope.sqlalchemy-1.1.tar.gz";
        sha256 = "81554c5b03fbf924c4144ef835b7900271fbd85cfe81cb6bd95e3ab7aa85189f";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."sqlalchemy"
        self."transaction"
        self."zope-interface"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/zope.sqlalchemy";
        license = licenses.zpl21;
        description = "Minimal Zope/SQLAlchemy transaction integration";
      };
    };
  };
  localOverridesFile = ./install_requirements_override.nix;
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
