# generated using pypi2nix tool (version: 2.0.4)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python38 -r ../python_requirements/test_requirements.txt --basename test_requirements
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

    "beautifulsoup4" = python.mkDerivation {
      name = "beautifulsoup4-4.9.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/3b/e4/7cfc641f11e0eef60123912611a5c9ee7d4638da7325878b695b9ae4bb6f/beautifulsoup4-4.9.0.tar.gz";
        sha256 = "594ca51a10d2b3443cbac41214e12dbb2a1cd57e1a7344659849e2e20ba6a8d8";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."soupsieve"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.crummy.com/software/BeautifulSoup/bs4/";
        license = licenses.mit;
        description = "Screen-scraping library";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2020.4.5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b8/e2/a3a86a67c3fc8249ed305fc7b7d290ebe5e4d46ad45573884761ef4dea7b/certifi-2020.4.5.1.tar.gz";
        sha256 = "51fcb31174be6e6664c5f69e3e1691a2d72a1a12e90f872cbdb1567eb47b6519";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifiio.readthedocs.io/en/latest/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
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

    "colorama" = python.mkDerivation {
      name = "colorama-0.4.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/75/f2a4c0c94c85e2693c229142eb448840fba0f9230111faa889d1f541d12d/colorama-0.4.3.tar.gz";
        sha256 = "e96da0d330793e2cb9485e9ddfd918d456036c7149416295932478192f4436a1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tartley/colorama";
        license = licenses.bsdOriginal;
        description = "Cross-platform colored terminal text.";
      };
    };

    "coverage" = python.mkDerivation {
      name = "coverage-5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fe/4d/3d892bdd21acba6c9e9bec6dc93fbe619883a0967c62f976122f2c6366f3/coverage-5.1.tar.gz";
        sha256 = "f90bfc4ad18450c80b024036eaf91e4a246ae287701aaa88eaebebf150868052";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/nedbat/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
      };
    };

    "factory-boy" = python.mkDerivation {
      name = "factory-boy-2.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5d/28/9f2284328547a3e29b39422a0a138d118a57686c0b4479f00c72240668d7/factory_boy-2.12.0.tar.gz";
        sha256 = "faf48d608a1735f0d0a3c9cbf536d64f9132b547dae7ba452c4d99a79e84a370";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."faker"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/FactoryBoy/factory_boy";
        license = licenses.mit;
        description = "A versatile test fixtures replacement based on thoughtbot's factory_bot for Ruby.";
      };
    };

    "faker" = python.mkDerivation {
      name = "faker-4.0.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/28/93/47a80b4b4478b5f38a4a3b704b836f2bb8c0392378bbf9146570fab1be3b/Faker-4.0.3.tar.gz";
        sha256 = "7292806948ed848f1bcea1e7b963bae6f398687d1da0ea096e156fea2787f454";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."python-dateutil"
        self."text-unidecode"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/joke2k/faker";
        license = licenses.mit;
        description = "Faker is a Python package that generates fake data for you.";
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

    "inflect" = python.mkDerivation {
      name = "inflect-4.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/18/29/2a0292362ea78760f95584ffd41e75b3d001d501c4627ba321d180a4fc0c/inflect-4.1.0.tar.gz";
        sha256 = "def6f3791be9181f0c01e0bf5949304007ec6e04c6674fbef7cc49c657b8a9a5";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jazzband/inflect";
        license = licenses.mit;
        description = "Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words";
      };
    };

    "inflection" = python.mkDerivation {
      name = "inflection-0.4.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e8/dc/3986343faf9631d8bc61d8a6a1331b5f4f08723dbce3b39f524c367a1621/inflection-0.4.0.tar.gz";
        sha256 = "32a5c3341d9583ec319548b9015b7fbdf8c429cbcb575d326c33ae3a0e90d52c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jpvanhal/inflection";
        license = licenses.mit;
        description = "A port of Ruby on Rails inflector to Python";
      };
    };

    "mimesis" = python.mkDerivation {
      name = "mimesis-3.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e5/ed/267379f02a01b60ef40cf36a9889ee300c54026ea2a2653cd246772b9441/mimesis-3.3.0.tar.gz";
        sha256 = "4b8fc414bd101109615fa8b6ad49f1811199e2745a4e9ef527193a4ab69637fc";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/lk-geimfari/mimesis";
        license = licenses.mit;
        description = "Mimesis: fake data generator.";
      };
    };

    "mimesis-factory" = python.mkDerivation {
      name = "mimesis-factory-1.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/db/ee/3c1716c2fdcab0c128f1d9b1a23dafd008547efcf31914bf8ddbedcbffc8/mimesis_factory-1.0.0.tar.gz";
        sha256 = "68f043a5066aa46e6746a097189d46d761b1e16521f78aeac6d5664fe365efb7";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."factory-boy"
        self."mimesis"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mimesis-lab/mimesis-factory";
        license = "UNKNOWN";
        description = "Mimesis integration with factory_boy";
      };
    };

    "more-itertools" = python.mkDerivation {
      name = "more-itertools-8.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a0/47/6ff6d07d84c67e3462c50fa33bf649cda859a8773b53dc73842e84455c05/more-itertools-8.2.0.tar.gz";
        sha256 = "b1ddb932186d8a6ac451e1d95844b382f55e12686d51ca0c68b6f61f2ab7a507";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/erikrose/more-itertools";
        license = licenses.mit;
        description = "More routines for operating on iterables, beyond itertools";
      };
    };

    "packaging" = python.mkDerivation {
      name = "packaging-20.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/65/37/83e3f492eb52d771e2820e88105f605335553fe10422cba9d256faeb1702/packaging-20.3.tar.gz";
        sha256 = "3c292b474fda1671ec57d46d739d072bfd495a4f51ad01a055121d81e952b7a3";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pyparsing"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/packaging";
        license = licenses.asl20;
        description = "Core utilities for Python packages";
      };
    };

    "pluggy" = python.mkDerivation {
      name = "pluggy-0.13.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-0.13.1.tar.gz";
        sha256 = "15b2acde666561e1298d71b523007ed7364de07029219b604cf808bfa1c765b0";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pluggy";
        license = licenses.mit;
        description = "plugin and hook calling mechanisms for python";
      };
    };

    "py" = python.mkDerivation {
      name = "py-1.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bd/8f/169d08dcac7d6e311333c96b63cbe92e7947778475e1a619b674989ba1ed/py-1.8.1.tar.gz";
        sha256 = "5e27081401262157467ad6e7f851b7aa402c5852dbcb3dae06768434de5752aa";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };

    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.4.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c1/47/dfc9c342c9842bbe0036c7f763d2d6686bcf5eb1808ba3e170afdb282210/pyparsing-2.4.7.tar.gz";
        sha256 = "c203ec8783bf771a155b207279b9bccb8dea02d8f0c9e5f8ead507bc3246ecc1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pyparsing/pyparsing/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };

    "pytest" = python.mkDerivation {
      name = "pytest-5.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6d/4e/572aed20422dee7fa2bd27995b2a53a32de90c1826e5531c9df6d3ea77ed/pytest-5.4.1.tar.gz";
        sha256 = "84dde37075b8805f3d1f392cc47e38a0e59518fb46a431cfdaf7cf1ce805f970";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."attrs"
        self."more-itertools"
        self."packaging"
        self."pluggy"
        self."py"
        self."wcwidth"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pytest.org/en/latest/";
        license = licenses.mit;
        description = "pytest: simple powerful testing with Python";
      };
    };

    "pytest-cov" = python.mkDerivation {
      name = "pytest-cov-2.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/13/8a/51f54b43a043c799bceca846594b9a310823a3e52df5ec27109cccba90f4/pytest-cov-2.8.1.tar.gz";
        sha256 = "cc6742d8bac45070217169f5f72ceee1e0e55b0221f54bcf24845972d3a47f2b";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."coverage"
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-cov";
        license = licenses.bsdOriginal;
        description = "Pytest plugin for measuring coverage.";
      };
    };

    "pytest-factoryboy" = python.mkDerivation {
      name = "pytest-factoryboy-2.0.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/77/8b/ec891cea6f61ac849bd68ff677ee2176eaec606fa1b7a7a4a80fa17ce6b1/pytest-factoryboy-2.0.3.tar.gz";
        sha256 = "ffef3fb7ddec1299d3df0d334846259023f3d1da5ab887ad880139a8253a5a1a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."factory-boy"
        self."inflection"
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-factoryboy";
        license = licenses.mit;
        description = "Factory Boy support for pytest.";
      };
    };

    "pytest-instafail" = python.mkDerivation {
      name = "pytest-instafail-0.4.1.post0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/4d/e7/f97308d60609536bfba9032201a507c29f282b49d0c209e10a5274f987ff/pytest-instafail-0.4.1.post0.tar.gz";
        sha256 = "cc5007720424aeabadcf178fc0aecb3b21e09950b9e93638f3eb16c47f5fa917";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-instafail";
        license = licenses.bsdOriginal;
        description = "py.test plugin to show failures instantly";
      };
    };

    "pytest-localserver" = python.mkDerivation {
      name = "pytest-localserver-0.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6c/b3/db8f8700718fbefaa2e8b2ef690fec147e560ce92e2300cdb3ff462d313c/pytest-localserver-0.5.0.tar.gz";
        sha256 = "3a5427909d1dfda10772c1bae4b9803679c0a8f04adb66c338ac607773bfefc2";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."werkzeug"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://bitbucket.org/pytest-dev/pytest-localserver/";
        license = licenses.mit;
        description = "py.test plugin to test server connections locally.";
      };
    };

    "pytest-mock" = python.mkDerivation {
      name = "pytest-mock-3.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bf/7f/259d29303ab4525deddda1d278d7a827d2fcbc2fe940913e31426e773377/pytest-mock-3.1.0.tar.gz";
        sha256 = "ce610831cedeff5331f4e2fc453a5dd65384303f680ab34bee2c6533855b431c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-mock/";
        license = licenses.mit;
        description = "Thin-wrapper around the mock package for easier use with pytest";
      };
    };

    "pytest-pspec" = python.mkDerivation {
      name = "pytest-pspec-0.0.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/78/c7/ae7ad32a39f30afbe9eb358df5c8a97d1d59aad34ebd3cd9e5e88325dce1/pytest-pspec-0.0.3.tar.gz";
        sha256 = "14274721d4b1ac500a7d133c7a84af26b921dbe942dbf175512ae16225647968";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytest"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gowtham-sai/pytest-pspec";
        license = licenses.mit;
        description = "A rspec format reporter for Python ptest";
      };
    };

    "python-dateutil" = python.mkDerivation {
      name = "python-dateutil-2.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/be/ed/5bbc91f03fa4c839c4c7360375da77f9659af5f7086b7a7bdda65771c8e0/python-dateutil-2.8.1.tar.gz";
        sha256 = "73ebfe9dbf22e832286dafa60473e4cd239f8592f699aa5adaf10050e6e1823c";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://dateutil.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Extensions to the standard Python datetime module";
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

    "responses" = python.mkDerivation {
      name = "responses-0.10.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/9c/45/32f8d8c0c8f1f3843419a36aee0815bad040ac0029cfe96bb894894f042d/responses-0.10.14.tar.gz";
        sha256 = "1a78bc010b20a5022a2c0cb76b8ee6dc1e34d887972615ebd725ab9a166a4960";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."requests"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/getsentry/responses";
        license = licenses.asl20;
        description = "A utility library for mocking out the `requests` Python library.";
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

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b2/f7/60a645aae001a2e06cf4b8db2fba9d9f36b8fd378f10647e3e218b61b74b/setuptools_scm-3.5.0.tar.gz";
        sha256 = "5bdf21a05792903cafe7ae0c9501182ab52497614fa6b1750d9dbae7b60c1a87";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
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

    "soupsieve" = python.mkDerivation {
      name = "soupsieve-2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/15/53/3692c565aea19f7d9dd696fee3d0062782e9ad5bf9535267180511a15967/soupsieve-2.0.tar.gz";
        sha256 = "e914534802d7ffd233242b785229d5ba0766a7f487385e3f714446a07bf540ae";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/facelessuser/soupsieve";
        license = licenses.mit;
        description = "A modern CSS selector implementation for Beautiful Soup.";
      };
    };

    "text-unidecode" = python.mkDerivation {
      name = "text-unidecode-1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ab/e2/e9a00f0ccb71718418230718b3d900e71a5d16e701a3dae079a21e9cd8f8/text-unidecode-1.3.tar.gz";
        sha256 = "bad6603bb14d279193107714b288be206cac565dfa49aa5b105294dd5c4aab93";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kmike/text-unidecode/";
        license = licenses.artistic2;
        description = "The most basic Text::Unidecode port";
      };
    };

    "toml" = python.mkDerivation {
      name = "toml-0.10.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b9/19/5cbd78eac8b1783671c40e34bb0fa83133a06d340a38b55c645076d40094/toml-0.10.0.tar.gz";
        sha256 = "229f81c57791a41d65e399fc06bf0848bab550a9dfd5ed66df18ce5f05e73d5c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/uiri/toml";
        license = licenses.mit;
        description = "Python Library for Tom's Obvious, Minimal Language";
      };
    };

    "typing-extensions" = python.mkDerivation {
      name = "typing-extensions-3.7.4.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6a/28/d32852f2af6b5ead85d396249d5bdf450833f3a69896d76eb480d9c5e406/typing_extensions-3.7.4.2.tar.gz";
        sha256 = "79ee589a3caca649a9bfd2a8de4709837400dfa00b6cc81962a1e6a1815969ae";
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

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.25.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/05/8c/40cd6949373e23081b3ea20d5594ae523e681b6f472e600fbc95ed046a36/urllib3-1.25.9.tar.gz";
        sha256 = "3018294ebefce6572a474f0604c2021e33b3fd8006ecd11d62107a5d2a963527";
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

    "waitress" = python.mkDerivation {
      name = "waitress-1.4.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/55/0b/f178246f1658a360aa1fb4ae3cb4905ff479fe85e8a58cd7c8bd27192342/waitress-1.4.3.tar.gz";
        sha256 = "045b3efc3d97c93362173ab1dfc159b52cfa22b46c3334ffc805dbdbf0e4309e";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/Pylons/waitress";
        license = licenses.zpl21;
        description = "Waitress WSGI server";
      };
    };

    "wcwidth" = python.mkDerivation {
      name = "wcwidth-0.1.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/25/9d/0acbed6e4a4be4fc99148f275488580968f44ddb5e69b8ceb53fc9df55a0/wcwidth-0.1.9.tar.gz";
        sha256 = "ee73862862a156bf77ff92b09034fc4825dd3af9cf81bc5b360668d425f3c5f1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jquast/wcwidth";
        license = licenses.mit;
        description = "Measures number of Terminal column cells of wide-character codes";
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

    "webtest" = python.mkDerivation {
      name = "webtest-2.0.35";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/97/87/73f7db7be3a33c5a7aa3772a4cdb309995dba28bddf7a41a56229f3b1507/WebTest-2.0.35.tar.gz";
        sha256 = "aac168b5b2b4f200af4e35867cf316712210e3d5db81c1cbdff38722647bb087";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."beautifulsoup4"
        self."six"
        self."waitress"
        self."webob"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pylonsproject.org/projects/webtest/en/latest/";
        license = licenses.mit;
        description = "Helper to test WSGI applications";
      };
    };

    "werkzeug" = python.mkDerivation {
      name = "werkzeug-1.0.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/10/27/a33329150147594eff0ea4c33c2036c0eadd933141055be0ff911f7f8d04/Werkzeug-1.0.1.tar.gz";
        sha256 = "6c80b1e5ad3665290ea39320b91e1be1e0d5f60652b964a3070216de83d2e47c";
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
  };
  localOverridesFile = ./test_requirements_override.nix;
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