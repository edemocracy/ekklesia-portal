# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python37 -r ../generated_requirements/frozen_test_requirements.txt --basename test_requirements
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
    "atomicwrites" = python.mkDerivation {
      name = "atomicwrites-1.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ec/0f/cd484ac8820fed363b374af30049adc8fd13065720fd4f4c6be8a2309da7/atomicwrites-1.3.0.tar.gz";
        sha256 = "75a9445bac02d8d058d5e1fe689654ba5a6556a1dfd8ce6ec55a0ed79866cfa6";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/untitaker/python-atomicwrites";
        license = licenses.mit;
        description = "Atomic file writes.";
      };
    };

    "attrs" = python.mkDerivation {
      name = "attrs-19.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bd/69/2833f182ea95ea1f17e9a7559b8b92ebfdf4f68b5c58b15bc10f47bc2e01/attrs-19.2.0.tar.gz";
        sha256 = "f913492e1663d3c36f502e5e9ba6cd13cf19d7fab50aa13239e420fef95e1396";
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

    "beautifulsoup4" = python.mkDerivation {
      name = "beautifulsoup4-4.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/23/7b/37a477bc668068c23cb83e84191ee03709f1fa24d957b7d95083f10dda14/beautifulsoup4-4.8.0.tar.gz";
        sha256 = "25288c9e176f354bf277c0a10aa96c782a6a18a17122dba2e8cec4a97e03343b";
};
      doCheck = commonDoCheck;
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

    "colorama" = python.mkDerivation {
      name = "colorama-0.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/76/53/e785891dce0e2f2b9f4b4ff5bc6062a53332ed28833c7afede841f46a5db/colorama-0.4.1.tar.gz";
        sha256 = "05eed71e2e327246ad6b38c540c4a3117230b19679b875190486ddd2d721422d";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tartley/colorama";
        license = licenses.bsdOriginal;
        description = "Cross-platform colored terminal text.";
      };
    };

    "coverage" = python.mkDerivation {
      name = "coverage-4.5.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/85/d5/818d0e603685c4a613d56f065a721013e942088047ff1027a632948bdae6/coverage-4.5.4.tar.gz";
        sha256 = "e07d9f1a23e9e93ab5c62902833bf3e4b1f65502927379148b6622686223125c";
};
      doCheck = commonDoCheck;
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
      name = "faker-2.0.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e6/44/735dd3ca245b9ac36659274767ddba71480e161e919530b9f891d2dd4a60/Faker-2.0.2.tar.gz";
        sha256 = "45cc9cca3de8beba5a2da3bd82a6e5544f53da1a702645c8485f682366c15026";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."python-dateutil"
        self."six"
        self."text-unidecode"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/joke2k/faker";
        license = licenses.mit;
        description = "Faker is a Python package that generates fake data for you.";
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

    "importlib-metadata" = python.mkDerivation {
      name = "importlib-metadata-0.23";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5d/44/636bcd15697791943e2dedda0dbe098d8530a38d113b202817133e0b06c0/importlib_metadata-0.23.tar.gz";
        sha256 = "aa18d7378b00b40847790e7c27e11673d7fed219354109d0e7b9e5b25dc3ad26";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [
        self."zipp"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://importlib-metadata.readthedocs.io/";
        license = "Apache Software License";
        description = "Read metadata from Python packages";
      };
    };

    "inflect" = python.mkDerivation {
      name = "inflect-2.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5e/79/fc91ef0768c6ac564c2d820ff2658b6a82686aeb71145980b71c50d0a122/inflect-2.1.0.tar.gz";
        sha256 = "4ded1b2a6fcf0fc0397419c7727f131a93b67b80d899f2973be7758628e12b73";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jazzband/inflect";
        license = "UNKNOWN";
        description = "Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words";
      };
    };

    "inflection" = python.mkDerivation {
      name = "inflection-0.3.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d5/35/a6eb45b4e2356fe688b21570864d4aa0d0a880ce387defe9c589112077f8/inflection-0.3.1.tar.gz";
        sha256 = "18ea7fb7a7d152853386523def08736aa8c32636b047ade55f7578c4edeb16ca";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/jpvanhal/inflection";
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
      name = "more-itertools-7.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c2/31/45f61c8927c9550109f1c4b99ba3ca66d328d889a9c9853a808bff1c9fa0/more-itertools-7.2.0.tar.gz";
        sha256 = "409cd48d4db7052af495b09dec721011634af3753ae1ef92d2b32f73a745f832";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/erikrose/more-itertools";
        license = licenses.mit;
        description = "More routines for operating on iterables, beyond itertools";
      };
    };

    "packaging" = python.mkDerivation {
      name = "packaging-19.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5a/2f/449ded84226d0e2fda8da9252e5ee7731bdf14cd338f622dfcd9934e0377/packaging-19.2.tar.gz";
        sha256 = "28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pyparsing"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/packaging";
        license = licenses.bsdOriginal;
        description = "Core utilities for Python packages";
      };
    };

    "pluggy" = python.mkDerivation {
      name = "pluggy-0.13.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d7/9d/ae82a5facf2dd89f557a33ad18eb68e5ac7b7a75cf52bf6a208f29077ecf/pluggy-0.13.0.tar.gz";
        sha256 = "fa5fa1622fa6dd5c030e9cad086fa19ef6a0cf6d7a2d12318e10cb49d6d68f34";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [
        self."importlib-metadata"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pluggy";
        license = licenses.mit;
        description = "plugin and hook calling mechanisms for python";
      };
    };

    "py" = python.mkDerivation {
      name = "py-1.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f1/5a/87ca5909f400a2de1561f1648883af74345fe96349f34f737cdfc94eba8c/py-1.8.0.tar.gz";
        sha256 = "dc639b046a6e2cff5bbe40194ad65936d6ba360b52b3c3fe1d08a82dd50b5e53";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };

    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.4.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7e/24/eaa8d7003aee23eda270099eeec754d7bf4399f75c6a011ef948304f66a2/pyparsing-2.4.2.tar.gz";
        sha256 = "6f98a7b9397e206d78cc01df10131398f1c8b8510a2f4d97d9abd82e1aacdd80";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pyparsing/pyparsing/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };

    "pytest" = python.mkDerivation {
      name = "pytest-5.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/77/92/7ef2e1685a676246a0380f5c0a27f8b8682920b7749ed096c4237aa1455a/pytest-5.1.1.tar.gz";
        sha256 = "c3d5020755f70c82eceda3feaf556af9a341334414a8eca521a18f463bcead88";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [
        self."atomicwrites"
        self."attrs"
        self."importlib-metadata"
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
      name = "pytest-cov-2.7.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bb/0f/3db7ff86801883b21d5353b258c994b1b8e2abbc804e2273b8d0fd19004b/pytest-cov-2.7.1.tar.gz";
        sha256 = "e00ea4fdde970725482f1f35630d12f074e121a23801aabf2ae154ec6bdd343a";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."coverage"
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-cov";
        license = licenses.mit;
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
      name = "pytest-instafail-0.4.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fa/16/473621ad68cc2a1cb2888478e66db5080a06adf695470c8dd4ec669c25d5/pytest-instafail-0.4.1.tar.gz";
        sha256 = "84c87dd708f00d248fb062cdfaf5ba14bf10ce68ce56d46d58f20aa882a33924";
};
      doCheck = commonDoCheck;
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
      name = "pytest-mock-1.10.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/18/01/92e33e69c1704bb26672f6043748c9ee3bb2d958bcf41cc8b9d447fa6746/pytest-mock-1.10.4.tar.gz";
        sha256 = "5bf5771b1db93beac965a7347dc81c675ec4090cb841e49d9d34637a25c30568";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-mock/";
        license = licenses.mit;
        description = "Thin-wrapper around the mock package for easier use with py.test";
      };
    };

    "pytest-pspec" = python.mkDerivation {
      name = "pytest-pspec-0.0.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/78/c7/ae7ad32a39f30afbe9eb358df5c8a97d1d59aad34ebd3cd9e5e88325dce1/pytest-pspec-0.0.3.tar.gz";
        sha256 = "14274721d4b1ac500a7d133c7a84af26b921dbe942dbf175512ae16225647968";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytest"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gowtham-sai/pytest-pspec";
        license = "UNKNOWN";
        description = "A rspec format reporter for Python ptest";
      };
    };

    "python-dateutil" = python.mkDerivation {
      name = "python-dateutil-2.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ad/99/5b2e99737edeb28c71bcbec5b5dda19d0d9ef3ca3e92e3e925e7c0bb364c/python-dateutil-2.8.0.tar.gz";
        sha256 = "c89805f6f4d64db21ed966fda138f8a5ed7a4fdbc1a8ee329ce1b74e3c74da9e";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://dateutil.readthedocs.io";
        license = "Dual License";
        description = "Extensions to the standard Python datetime module";
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

    "responses" = python.mkDerivation {
      name = "responses-0.10.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cb/83/9a79053228532392949542bb21ee3e685e089ac8dc2fe7f0a9dfbbced0e5/responses-0.10.6.tar.gz";
        sha256 = "502d9c0c8008439cfcdef7e251f507fcfdd503b56e8c0c87c3c3e3393953f790";
};
      doCheck = commonDoCheck;
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

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.3.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/83/44/53cad68ce686585d12222e6769682c4bdb9686808d2739671f9175e2938b/setuptools_scm-3.3.3.tar.gz";
        sha256 = "bd25e1fb5e4d603dcf490f1fde40fb4c595b357795674c3e5cb7f6217ab39ea5";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
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

    "soupsieve" = python.mkDerivation {
      name = "soupsieve-1.9.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7f/4e/95a13527e18b6f1a15c93f1c634b86d5fa634c5619dce695f4e0cd68182f/soupsieve-1.9.4.tar.gz";
        sha256 = "605f89ad5fdbfefe30cdc293303665eff2d188865d4dbe4eb510bba1edfbfce3";
};
      doCheck = commonDoCheck;
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
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kmike/text-unidecode/";
        license = "Artistic License";
        description = "The most basic Text::Unidecode port";
      };
    };

    "typing-extensions" = python.mkDerivation {
      name = "typing-extensions-3.7.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/59/b6/21774b993eec6e797fbc49e53830df823b69a3cb62f94d36dfb497a0b65a/typing_extensions-3.7.4.tar.gz";
        sha256 = "2ed632b30bb54fc3941c382decfd0ee4148f5c591651c9272473fea2c6397d95";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/python/typing/blob/master/typing_extensions/README.rst";
        license = "PSF";
        description = "Backported and Experimental Type Hints for Python 3.5+";
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

    "waitress" = python.mkDerivation {
      name = "waitress-1.3.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a6/e6/708da7bba65898e5d759ade8391b1077e49d07be0b0223c39f5be04def56/waitress-1.3.1.tar.gz";
        sha256 = "278e09d6849acc1365404bbf7d790d0423b159802e850c726e8cd0a126a2dac7";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/Pylons/waitress";
        license = licenses.zpl21;
        description = "Waitress WSGI server";
      };
    };

    "wcwidth" = python.mkDerivation {
      name = "wcwidth-0.1.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/55/11/e4a2bb08bb450fdbd42cc709dd40de4ed2c472cf0ccb9e64af22279c5495/wcwidth-0.1.7.tar.gz";
        sha256 = "3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jquast/wcwidth";
        license = licenses.mit;
        description = "Measures number of Terminal column cells of wide-character codes";
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

    "webtest" = python.mkDerivation {
      name = "webtest-2.0.33";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a8/b0/ffc9413b637dbe26e291429bb0f6ed731e518d0cd03da28524a8fe2e8a8f/WebTest-2.0.33.tar.gz";
        sha256 = "41348efe4323a647a239c31cde84e5e440d726ca4f449859264e538d39037fd0";
};
      doCheck = commonDoCheck;
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
        license = licenses.bsd3;
        description = "The comprehensive WSGI web application library.";
      };
    };

    "zipp" = python.mkDerivation {
      name = "zipp-0.6.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/57/dd/585d728479d97d25aeeb9aa470d36a4ad8d0ba5610f84e14770128ce6ff7/zipp-0.6.0.tar.gz";
        sha256 = "3718b1cbcd963c7d4c5511a8240812904164b7f381b647143a89d3b98f9bcd8e";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [
        self."more-itertools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jaraco/zipp";
        license = "UNKNOWN";
        description = "Backport of pathlib-compatible object wrapper for zip files";
      };
    };
  };
  localOverridesFile = ./test_requirements_override.nix;
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
