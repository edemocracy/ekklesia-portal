# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -V 3.6 -r install_requirements.txt -r test_requirements.txt -r devel_requirements.txt -r setup_requirements.txt -E postgresql -E libffi
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python36;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            sed -i               -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"                  $out/${pkgs.python35.sitePackages}/pip/req/req_install.py
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql libffi ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python36-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
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
          ln -s ${pythonPackages.python.executable}               python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs //                                            { meta = drv.meta; });
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "Babel" = python.mkDerivation {
      name = "Babel-2.5.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/5a/22/63f1dbb8514bb7e0d0c8a85cc9b14506599a075e231985f98afd70430e1f/Babel-2.5.1.tar.gz"; sha256 = "6007daf714d0cd5524bbe436e2d42b3c20e68da66289559341e48d2cd6d25811"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pytz"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://babel.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "Internationalization utilities";
      };
    };



    "Flask" = python.mkDerivation {
      name = "Flask-0.12.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/eb/12/1c7bd06fcbd08ba544f25bf2c6612e305a70ea51ca0eda8007344ec3f123/Flask-0.12.2.tar.gz"; sha256 = "49f44461237b69ecd901cc7ce66feea0319b9158743dd27a2899962ab214dac1"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Jinja2"
      self."Werkzeug"
      self."click"
      self."itsdangerous"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/pallets/flask/";
        license = licenses.bsdOriginal;
        description = "A microframework based on Werkzeug, Jinja2 and good intentions";
      };
    };



    "Flask-Admin" = python.mkDerivation {
      name = "Flask-Admin-1.5.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/b5/90/664f46eb4187e9f5ab3dafa1a2043eb7772c01c7aaf5072b7e4ac6213533/Flask-Admin-1.5.0.tar.gz"; sha256 = "fe3a96d99f22e293cd7e83d364de6cffd36573ef25db93d6e32102527a624bc5"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."WTForms"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/flask-admin/flask-admin/";
        license = licenses.bsdOriginal;
        description = "Simple and extensible admin interface framework for Flask";
      };
    };



    "Flask-BabelEx" = python.mkDerivation {
      name = "Flask-BabelEx-0.9.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/80/ad/cc2b0becd98050eed775ca85d6e5fa784547acff69f968183098df8a52b3/Flask-BabelEx-0.9.3.tar.gz"; sha256 = "cf79cdedb5ce860166120136b0e059e9d97b8df07a3bc2411f6243de04b754b4"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Babel"
      self."Flask"
      self."Jinja2"
      self."speaklater"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mrjoes/flask-babelex";
        license = licenses.bsdOriginal;
        description = "Adds i18n/l10n support to Flask applications";
      };
    };



    "Flask-Dance" = python.mkDerivation {
      name = "Flask-Dance-0.13.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/11/d7/fbbec95ad07cc1c3946b8015cc2f57a7b7c643ae35289f2faf8ed944e612/Flask-Dance-0.13.0.tar.gz"; sha256 = "507496b730a90365bb49e3e9dd4f9351b9595100acab66020831f7987ba99f11"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."SQLAlchemy"
      self."SQLAlchemy-Utils"
      self."URLObject"
      self."blinker"
      self."lazy"
      self."oauthlib"
      self."requests"
      self."requests-oauthlib"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/singingwolfboy/flask-dance";
        license = licenses.mit;
        description = "Doing the OAuth dance with style using Flask, requests, and oauthlib";
      };
    };



    "Flask-Login" = python.mkDerivation {
      name = "Flask-Login-0.4.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/70/96/20cae731ef27084dcb183f3a6e3073d0232f10c1fd7be76729bd7bd4b994/Flask-Login-0.4.0.tar.gz"; sha256 = "d25e356b14a59f52da0ab30c31c2ad285fa23a840f0f6971df7ed247c77082a7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/maxcountryman/flask-login";
        license = licenses.mit;
        description = "User session management for Flask";
      };
    };



    "Flask-Misaka" = python.mkDerivation {
      name = "Flask-Misaka-0.4.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3d/19/71e8dc5c537f6a4e3b9ae2836f442a8643c2ce900eafd2484ef18ad87cb3/Flask-Misaka-0.4.1.tar.gz"; sha256 = "1dad09a312aafc3783dd4228bcc60708e339494c1653d6bb8e1936b5c4fdeaac"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."misaka"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/singingwolfboy/flask-misaka/";
        license = licenses.mit;
        description = "A pleasant interface between the Flask web framework and the Misaka Markdown parser.";
      };
    };



    "Flask-SQLAlchemy" = python.mkDerivation {
      name = "Flask-SQLAlchemy-2.3.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3a/66/f5ace276517c075f102457dd2f7d8645b033758f9c6effb4e0970a90fec1/Flask-SQLAlchemy-2.3.2.tar.gz"; sha256 = "5971b9852b5888655f11db634e87725a9031e170f37c0ce7851cf83497f56e53"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."SQLAlchemy"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/flask-sqlalchemy";
        license = licenses.bsdOriginal;
        description = "Adds SQLAlchemy support to your Flask application";
      };
    };



    "Flask-Sijax" = python.mkDerivation {
      name = "Flask-Sijax-0.4.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/97/0e/b2c803d8af324c7161608339496b7a8b05af4711d3da329f8e8d7fc7c49d/Flask-Sijax-0.4.1.tar.gz"; sha256 = "fb2bf2d4f75408185102195055d75549fee8d9c9e954dca2427186925cdc429f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."Sijax"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/spantaleev/flask-sijax";
        license = licenses.bsdOriginal;
        description = "An extension for the Flask microframework that adds Sijax support.";
      };
    };



    "Flask-WTF" = python.mkDerivation {
      name = "Flask-WTF-0.14.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/ba/15/00a9693180f214225a2c0b1bb9077f3b0b21f2e86522cbba22e8ad6e570c/Flask-WTF-0.14.2.tar.gz"; sha256 = "5d14d55cfd35f613d99ee7cba0fc3fbbe63ba02f544d349158c14ca15561cc36"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Flask"
      self."WTForms"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/lepture/flask-wtf";
        license = licenses.bsdOriginal;
        description = "Simple integration of Flask and WTForms.";
      };
    };



    "Jinja2" = python.mkDerivation {
      name = "Jinja2-2.10";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz"; sha256 = "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Babel"
      self."MarkupSafe"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://jinja.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "A small but fast and easy to use stand-alone template engine written in pure python.";
      };
    };



    "MarkupSafe" = python.mkDerivation {
      name = "MarkupSafe-1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz"; sha256 = "a6be69091dac236ea9c6bc7d012beab42010fa914c459791d627dad4910eb665"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/pallets/markupsafe";
        license = licenses.bsdOriginal;
        description = "Implements a XML/HTML/XHTML Markup safe string for Python";
      };
    };



    "PyYAML" = python.mkDerivation {
      name = "PyYAML-3.12";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz"; sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pyyaml.org/wiki/PyYAML";
        license = licenses.mit;
        description = "YAML parser and emitter for Python";
      };
    };



    "Pygments" = python.mkDerivation {
      name = "Pygments-2.2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/71/2a/2e4e77803a8bd6408a2903340ac498cb0a2181811af7c9ec92cb70b0308a/Pygments-2.2.0.tar.gz"; sha256 = "dbae1046def0efb574852fab9e90209b23f556367b5a320c0bcb871c77c3e8cc"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pygments.org/";
        license = licenses.bsdOriginal;
        description = "Pygments is a syntax highlighting package written in Python.";
      };
    };



    "SQLAlchemy" = python.mkDerivation {
      name = "SQLAlchemy-1.1.15";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/c2/f6/11fcc1ce19a7cb81b1c9377f4e27ce3813265611922e355905e57c44d164/SQLAlchemy-1.1.15.tar.gz"; sha256 = "8b79a5ed91cdcb5abe97b0045664c55c140aec09e5dd5c01303e23de5fe7a95a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."psycopg2"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.sqlalchemy.org";
        license = licenses.mit;
        description = "Database Abstraction Library";
      };
    };



    "SQLAlchemy-Searchable" = python.mkDerivation {
      name = "SQLAlchemy-Searchable-0.10.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/77/7c/e767325f3a666095fda7f97cd611c6ab47b27d23c9db8bf3b755f0d2e8a3/SQLAlchemy-Searchable-0.10.6.tar.gz"; sha256 = "84f0bff434a17d64e8f7f394065b21855bd3c8a3ede770a25c84127e5d0f95f7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."SQLAlchemy"
      self."SQLAlchemy-Utils"
      self."psycopg2"
      self."pyparsing"
      self."pytest"
      self."validators"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-searchable";
        license = licenses.bsdOriginal;
        description = "Provides fulltext search capabilities for declarative SQLAlchemy models.";
      };
    };



    "SQLAlchemy-Utils" = python.mkDerivation {
      name = "SQLAlchemy-Utils-0.32.21";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/6b/8c/bf6539a85705e845e9f83908cc290dd34c352d90d9a86134124bd4b64acd/SQLAlchemy-Utils-0.32.21.tar.gz"; sha256 = "e35431b0e57c4f7030ff598c23813c8b7b04b508ce10e8e9ebe448645b38d6d7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Babel"
      self."Jinja2"
      self."Pygments"
      self."SQLAlchemy"
      self."psycopg2"
      self."pytest"
      self."pytz"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-utils";
        license = licenses.bsdOriginal;
        description = "Various utility functions for SQLAlchemy.";
      };
    };



    "Sijax" = python.mkDerivation {
      name = "Sijax-0.3.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3a/08/32c4e77caafc7542195cfb00e0ee400f1d9e29c4259842c3b32441b39bd3/Sijax-0.3.2.tar.gz"; sha256 = "11b062f4a8b2aad95c87e7c09e5daf5a6b0d0f08abf9efe5f91a0075c6be7c0d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."future"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/spantaleev/sijax-python";
        license = licenses.bsdOriginal;
        description = "An easy to use AJAX library based on jQuery.ajax";
      };
    };



    "URLObject" = python.mkDerivation {
      name = "URLObject-2.4.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/e2/b8/1d0a916f4b34c4618846e6da0e4eeaa8fcb4a2f39e006434fe38acb74b34/URLObject-2.4.3.tar.gz"; sha256 = "47b2e20e6ab9c8366b2f4a3566b6ff4053025dad311c4bb71279bbcfa2430caa"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/zacharyvoase/urlobject";
        license = licenses.publicDomain;
        description = "A utility class for manipulating URLs.";
      };
    };



    "WTForms" = python.mkDerivation {
      name = "WTForms-2.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/bf/91/2e553b86c55e9cf2f33265de50e052441fb753af46f5f20477fe9c61280e/WTForms-2.1.zip"; sha256 = "ffdf10bd1fa565b8233380cb77a304cd36fd55c73023e91d4b803c96bc11d46f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Babel"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://wtforms.simplecodes.com/";
        license = licenses.bsdOriginal;
        description = "A flexible forms validation and rendering library for python web development.";
      };
    };



    "WebOb" = python.mkDerivation {
      name = "WebOb-1.7.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/46/87/2f96d8d43b2078fae6e1d33fa86b95c228cebed060f4e3c7576cc44ea83b/WebOb-1.7.3.tar.gz"; sha256 = "e65ca14b9f5ae5b031988ffc93f8b7f305ddfcf17a4c774ae0db47bcb3b87283"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };



    "WebTest" = python.mkDerivation {
      name = "WebTest-2.0.29";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/94/de/8f94738be649997da99c47b104aa3c3984ecec51a1d8153ed09638253d56/WebTest-2.0.29.tar.gz"; sha256 = "dbbccc15ac2465066c95dc3a7de0d30cde3791e886ccbd7e91d5d2a2580c922d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."WebOb"
      self."beautifulsoup4"
      self."coverage"
      self."six"
      self."waitress"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webtest.pythonpaste.org/";
        license = licenses.mit;
        description = "Helper to test WSGI applications";
      };
    };



    "Werkzeug" = python.mkDerivation {
      name = "Werkzeug-0.12.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/56/41/c095a77eb2dd69bf278dd664a97d3416af04e9ba1a00b8c138f772741d31/Werkzeug-0.12.2.tar.gz"; sha256 = "903a7b87b74635244548b30d30db4c8947fe64c5198f58899ddcd3a13c23bb26"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://werkzeug.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "The Swiss Army knife of Python web development";
      };
    };



    "beautifulsoup4" = python.mkDerivation {
      name = "beautifulsoup4-4.6.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/fa/8d/1d14391fdaed5abada4e0f63543fef49b8331a34ca60c88bd521bcf7f782/beautifulsoup4-4.6.0.tar.gz"; sha256 = "808b6ac932dccb0a4126558f7dfdcf41710dd44a4ef497a0bb59a77f9f078e89"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.crummy.com/software/BeautifulSoup/bs4/";
        license = licenses.mit;
        description = "Screen-scraping library";
      };
    };



    "blinker" = python.mkDerivation {
      name = "blinker-1.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/1b/51/e2a9f3b757eb802f61dc1f2b09c8c99f6eb01cf06416c0671253536517b6/blinker-1.4.tar.gz"; sha256 = "471aee25f3992bd325afa3772f1063dbdbbca947a041b8b89466dc00d606f8b6"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/blinker/";
        license = licenses.mit;
        description = "Fast, simple object-to-object and broadcast signaling";
      };
    };



    "certifi" = python.mkDerivation {
      name = "certifi-2017.11.5";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/23/3f/8be01c50ed24a4bd6b8da799839066ce0288f66f5e11f0367323467f0cbc/certifi-2017.11.5.tar.gz"; sha256 = "5ec74291ca1136b40f0379e1128ff80e866597e4e2c1e755739a913bbc3613c0"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };



    "cffi" = python.mkDerivation {
      name = "cffi-1.11.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/c9/70/89b68b6600d479034276fed316e14b9107d50a62f5627da37fafe083fde3/cffi-1.11.2.tar.gz"; sha256 = "ab87dd91c0c4073758d07334c1e5f712ce8fe48f007b86f8238773963ee700a6"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pycparser"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://cffi.readthedocs.org";
        license = licenses.mit;
        description = "Foreign Function Interface for Python calling C code.";
      };
    };



    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"; sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };



    "click" = python.mkDerivation {
      name = "click-6.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/95/d9/c3336b6b5711c3ab9d1d3a80f1a3e2afeb9d8c02a7166462f6cc96570897/click-6.7.tar.gz"; sha256 = "f15516df478d5a56180fbf80e68f206010e6d160fc39fa508b65e035fd75130b"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/click";
        license = licenses.bsdOriginal;
        description = "A simple wrapper around optparse for powerful command line utilities.";
      };
    };



    "coverage" = python.mkDerivation {
      name = "coverage-4.4.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/0b/e1/190ef1a264144c9b073b7353c259ca5431b5ddc8861b452e858fcbd0e9de/coverage-4.4.2.tar.gz"; sha256 = "309d91bd7a35063ec7a0e4d75645488bfab3f0b66373e7722f23da7f5b0f34cc"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ned/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
      };
    };



    "decorator" = python.mkDerivation {
      name = "decorator-4.1.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/bb/e0/f6e41e9091e130bf16d4437dabbac3993908e4d6485ecbc985ef1352db94/decorator-4.1.2.tar.gz"; sha256 = "7cb64d38cb8002971710c8899fbdfb859a23a364b7c99dab19d1f719c2ba16b5"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/micheles/decorator";
        license = licenses.bsdOriginal;
        description = "Better living through Python with decorators";
      };
    };



    "future" = python.mkDerivation {
      name = "future-0.16.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/00/2b/8d082ddfed935f3608cc61140df6dcbf0edea1bc3ab52fb6c29ae3e81e85/future-0.16.0.tar.gz"; sha256 = "e39ced1ab767b5936646cedba8bcce582398233d6a627067d4c6a454c90cfedb"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://python-future.org";
        license = licenses.mit;
        description = "Clean single-source support for Python 3 and 2";
      };
    };



    "idna" = python.mkDerivation {
      name = "idna-2.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/f4/bd/0467d62790828c23c47fc1dfa1b1f052b24efdf5290f071c7a91d0d82fd3/idna-2.6.tar.gz"; sha256 = "2c6a5de3089009e3da7c5dde64a141dbc8551d5b7f6cf4ed7c2568d0cc520a8f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };



    "ipdb" = python.mkDerivation {
      name = "ipdb-0.10.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/ad/cc/0e7298e1fbf2efd52667c9354a12aa69fb6f796ce230cca03525051718ef/ipdb-0.10.3.tar.gz"; sha256 = "9ea256b4280fbe12840fb9dfc3ce498c6c6de03352eca293e4400b0dfbed2b28"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."ipython"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/gotcha/ipdb";
        license = licenses.bsdOriginal;
        description = "IPython-enabled pdb";
      };
    };



    "ipython" = python.mkDerivation {
      name = "ipython-6.2.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/fa/50/974211502bd72873728d44c3013fe79875c819c8fb69f778bcfd67bc7d38/ipython-6.2.1.tar.gz"; sha256 = "51c158a6c8b899898d1c91c6b51a34110196815cc905f9be0fa5878e19355608"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Pygments"
      self."decorator"
      self."jedi"
      self."pexpect"
      self."pickleshare"
      self."prompt-toolkit"
      self."requests"
      self."simplegeneric"
      self."traitlets"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://ipython.org";
        license = licenses.bsdOriginal;
        description = "IPython: Productive Interactive Computing";
      };
    };



    "ipython-genutils" = python.mkDerivation {
      name = "ipython-genutils-0.2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/e8/69/fbeffffc05236398ebfcfb512b6d2511c622871dca1746361006da310399/ipython_genutils-0.2.0.tar.gz"; sha256 = "eb2e116e75ecef9d4d228fdc66af54269afa26ab4463042e33785b887c628ba8"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://ipython.org";
        license = licenses.bsdOriginal;
        description = "Vestigial utilities from IPython";
      };
    };



    "itsdangerous" = python.mkDerivation {
      name = "itsdangerous-0.24";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz"; sha256 = "cbb3fcf8d3e33df861709ecaf89d9e6629cff0a217bc2848f1b41cd30d360519"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/itsdangerous";
        license = licenses.bsdOriginal;
        description = "Various helpers to pass trusted data to untrusted environments and back.";
      };
    };



    "jedi" = python.mkDerivation {
      name = "jedi-0.11.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/08/8d/34b133dfa210b55e7efaa8b09c736a8f4383fcda0b6487fc43a1db3c7ee7/jedi-0.11.0.tar.gz"; sha256 = "f6d5973573e76b1fd2ea75f6dcd6445d02d41ff3af5fc61b275b4e323d1dd396"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."parso"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/davidhalter/jedi";
        license = licenses.mit;
        description = "An autocompletion tool for Python that can be used for text editors.";
      };
    };



    "lazy" = python.mkDerivation {
      name = "lazy-1.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/10/3b/655ffabb1627bff2539ddc3f3e0cdd6df51c65d4d51c20ba4c14e1ee8ad4/lazy-1.3.zip"; sha256 = "c80a77bf7106ba7b27378759900cfefef38271088dc63b014bcfe610c8e68e3d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/stefanholek/lazy";
        license = licenses.bsdOriginal;
        description = "Lazy attributes for Python objects";
      };
    };



    "misaka" = python.mkDerivation {
      name = "misaka-2.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/47/c2/ba9c82ae0ec62bcec62d690e715be6ead4457f83000f4ef6e919f77a8e5f/misaka-2.1.0.tar.gz"; sha256 = "87637d90f5f52595d07ed1be93d0576d32632d125694b96b8e4ce55cd4c019fb"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."cffi"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/FSX/misaka";
        license = licenses.mit;
        description = "A CFFI binding for Hoedown, a markdown parsing library.";
      };
    };



    "oauthlib" = python.mkDerivation {
      name = "oauthlib-2.0.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/a5/8a/212e9b47fb54be109f3ff0684165bb38c51117f34e175c379fce5c7df754/oauthlib-2.0.6.tar.gz"; sha256 = "ce57b501e906ff4f614e71c36a3ab9eacbb96d35c24d1970d2539bbc3ec70ce1"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."blinker"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/idan/oauthlib";
        license = licenses.bsdOriginal;
        description = "A generic, spec-compliant, thorough implementation of the OAuth request-signing logic";
      };
    };



    "parso" = python.mkDerivation {
      name = "parso-0.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/32/f4/9f1ee3fc5f7a23aee6454feeadef423ef1aed405208135e81620b4e3ba77/parso-0.1.0.tar.gz"; sha256 = "c5279916bb417aa2bf634648ff895cf35dce371d7319744884827bfad06f8d7b"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/davidhalter/parso";
        license = licenses.mit;
        description = "A Python Parser";
      };
    };



    "pexpect" = python.mkDerivation {
      name = "pexpect-4.3.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/f8/44/5466c30e49762bb92e442bbdf4472d6904608d211258eb3198a11f0309a4/pexpect-4.3.0.tar.gz"; sha256 = "00ab0872f80f5db740499e7a1283a7c3b97bea542d72df84d83dea17d0afd2d9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."ptyprocess"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pexpect.readthedocs.io/";
        license = licenses.isc;
        description = "Pexpect allows easy control of interactive console applications.";
      };
    };



    "pickleshare" = python.mkDerivation {
      name = "pickleshare-0.7.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/69/fe/dd137d84daa0fd13a709e448138e310d9ea93070620c9db5454e234af525/pickleshare-0.7.4.tar.gz"; sha256 = "84a9257227dfdd6fe1b4be1319096c20eb85ff1e82c7932f36efccfe1b09737b"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pickleshare/pickleshare";
        license = licenses.mit;
        description = "Tiny 'shelve'-like database with concurrency support";
      };
    };



    "prompt-toolkit" = python.mkDerivation {
      name = "prompt-toolkit-1.0.15";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/8a/ad/cf6b128866e78ad6d7f1dc5b7f99885fb813393d9860778b2984582e81b5/prompt_toolkit-1.0.15.tar.gz"; sha256 = "858588f1983ca497f1cf4ffde01d978a3ea02b01c8a26a8bbc5cd2e66d816917"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
      self."wcwidth"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jonathanslenders/python-prompt-toolkit";
        license = licenses.bsdOriginal;
        description = "Library for building powerful interactive command lines in Python";
      };
    };



    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.7.3.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/dd/47/000b405d73ca22980684fd7bd3318690cc03cfa3b2ae1c5b7fff8050b28a/psycopg2-2.7.3.2.tar.gz"; sha256 = "5c3213be557d0468f9df8fe2487eaf2990d9799202c5ff5cb8d394d09fad9b2a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };



    "ptyprocess" = python.mkDerivation {
      name = "ptyprocess-0.5.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/51/83/5d07dc35534640b06f9d9f1a1d2bc2513fb9cc7595a1b0e28ae5477056ce/ptyprocess-0.5.2.tar.gz"; sha256 = "e64193f0047ad603b71f202332ab5527c5e52aa7c8b609704fc28c0dc20c4365"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pexpect/ptyprocess";
        license = "";
        description = "Run a subprocess in a pseudo terminal";
      };
    };



    "py" = python.mkDerivation {
      name = "py-1.4.34";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/68/35/58572278f1c097b403879c1e9369069633d1cbad5239b9057944bb764782/py-1.4.34.tar.gz"; sha256 = "0f2d585d22050e90c7d293b6451c83db097df77871974d90efd5a30dc12fcde3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };



    "pycparser" = python.mkDerivation {
      name = "pycparser-2.18";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/8c/2d/aad7f16146f4197a11f8e91fb81df177adcc2073d36a17b1491fd09df6ed/pycparser-2.18.tar.gz"; sha256 = "99a8ca03e29851d96616ad0404b4aad7d9ee16f25c9f9708a11faf2810f7b226"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/eliben/pycparser";
        license = licenses.bsdOriginal;
        description = "C parser in Python";
      };
    };



    "pyjade" = python.mkDerivation {
      name = "pyjade-4.0.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4a/04/396ec24e806fd3af7ea5d0f3cb6c7bbd4d00f7064712e4dd48f24c02ca95/pyjade-4.0.0.tar.gz"; sha256 = "8d95b741de09c4942259fc3d1ad7b4f48166e69cef6f11c172e4b2c458b1ccd7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/syrusakbary/pyjade";
        license = licenses.mit;
        description = "Jade syntax template adapter for Django, Jinja2, Mako and Tornado templates";
      };
    };



    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3c/ec/a94f8cf7274ea60b5413df054f82a8980523efd712ec55a59e7c3357cf7c/pyparsing-2.2.0.tar.gz"; sha256 = "0832bcf47acd283788593e7a0f542407bd9550a55a8a8435214a1960e04bcb04"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pyparsing.wikispaces.com/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };



    "pytest" = python.mkDerivation {
      name = "pytest-3.2.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/36/85/9b92d1c31c42fdc8a57d4e36d4c8e383caa3ce48f4c134d5c51d1efa8e1c/pytest-3.2.4.tar.gz"; sha256 = "f50c9d0e07f0b028f6046448cd7b66bd48ff4ed004641db3ea2898af3b9eaeee"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."py"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pytest.org";
        license = licenses.mit;
        description = "pytest: simple powerful testing with Python";
      };
    };



    "pytest-localserver" = python.mkDerivation {
      name = "pytest-localserver-0.3.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/41/d6/90242691486b2fc42cd2dd73023760a065263d5551ef34f8e209b6fa8576/pytest-localserver-0.3.7.tar.gz"; sha256 = "d828d79232456d0b4eb863e9de2c85699259f436a3185e39d0d5001b8c8521b0"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Werkzeug"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://bitbucket.org/pytest-dev/pytest-localserver/";
        license = licenses.mit;
        description = "py.test plugin to test server connections locally.";
      };
    };



    "pytest-runner" = python.mkDerivation {
      name = "pytest-runner-3.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/65/b4/ae89338cd2d81e2cc54bd6db2e962bfe948f612303610d68ab24539ac2d1/pytest-runner-3.0.tar.gz"; sha256 = "0f7c3a3cf5aead13f54baaa01ceb49e5ae92aba5d3ff1928e81e189c40bc6703"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-runner";
        license = licenses.mit;
        description = "Invoke py.test as distutils command with dependency resolution";
      };
    };



    "pytz" = python.mkDerivation {
      name = "pytz-2017.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/60/88/d3152c234da4b2a1f7a989f89609ea488225eaea015bc16fbde2b3fdfefa/pytz-2017.3.zip"; sha256 = "fae4cffc040921b8a2d60c6cf0b5d662c1190fe54d718271db4eb17d44a185b7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
      };
    };



    "requests" = python.mkDerivation {
      name = "requests-2.18.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/b0/e1/eab4fc3752e3d240468a8c0b284607899d2fbfb236a56b7377a329aa8d09/requests-2.18.4.tar.gz"; sha256 = "9c443e7324ba5b85070c4a818ade28bfabedf16ea10206da1132edaa6dda237e"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
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
      name = "requests-oauthlib-0.8.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/80/14/ad120c720f86c547ba8988010d5186102030591f71f7099f23921ca47fe5/requests-oauthlib-0.8.0.tar.gz"; sha256 = "883ac416757eada6d3d07054ec7092ac21c7f35cb1d2cf82faf205637081f468"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
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



    "setuptools-git" = python.mkDerivation {
      name = "setuptools-git-1.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/d9/c5/396c2c06cc89d4ce2d8ccf1d7e6cf31b33d4466a7c65a67a992adb3c6f29/setuptools-git-1.2.tar.gz"; sha256 = "ff64136da01aabba76ae88b050e7197918d8b2139ccbf6144e14d472b9c40445"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/wichert/setuptools-git";
        license = licenses.bsdOriginal;
        description = "Setuptools revision control system plugin for Git";
      };
    };



    "simplegeneric" = python.mkDerivation {
      name = "simplegeneric-0.8.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3d/57/4d9c9e3ae9a255cd4e1106bb57e24056d3d0709fc01b2e3e345898e49d5b/simplegeneric-0.8.1.zip"; sha256 = "dc972e06094b9af5b855b3df4a646395e43d1c9d0d39ed345b7393560d0b9173"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://cheeseshop.python.org/pypi/simplegeneric";
        license = licenses.zpl21;
        description = "Simple generic functions (similar to Python's own len(), pickle.dump(), etc.)";
      };
    };



    "six" = python.mkDerivation {
      name = "six-1.11.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz"; sha256 = "70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/six/";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "speaklater" = python.mkDerivation {
      name = "speaklater-1.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/11/92/5ae1effe0ccb8561c034a0111d53c8788660ddb7ed4992f0da1bb5c525e5/speaklater-1.3.tar.gz"; sha256 = "59fea336d0eed38c1f0bf3181ee1222d0ef45f3a9dd34ebe65e6bfffdd6a65a9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/speaklater";
        license = licenses.bsdOriginal;
        description = "implements a lazy string for python useful for use with gettext";
      };
    };



    "traitlets" = python.mkDerivation {
      name = "traitlets-4.3.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/a5/98/7f5ef2fe9e9e071813aaf9cb91d1a732e0a68b6c44a32b38cb8e14c3f069/traitlets-4.3.2.tar.gz"; sha256 = "9c4bd2d267b7153df9152698efb1050a5d84982d3384a37b2c1f7723ba3e7835"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."decorator"
      self."ipython-genutils"
      self."pytest"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://ipython.org";
        license = licenses.bsdOriginal;
        description = "Traitlets Python config system";
      };
    };



    "urllib3" = python.mkDerivation {
      name = "urllib3-1.22";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/ee/11/7c59620aceedcc1ef65e156cc5ce5a24ef87be4107c2b74458464e437a5d/urllib3-1.22.tar.gz"; sha256 = "cc44da8e1145637334317feebd728bd869a35285b93cbb4cca2577da7e62db4f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
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
      name = "validators-0.12.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/8f/b5/9c9bf9cc9b50acea54a175eee97b0092f7676dbd6a17e00591588640acc3/validators-0.12.0.tar.gz"; sha256 = "bf1aa66554df0a7907f0e78b6d356e2ce30d6f2e73fefd1f3b14d20114341066"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."decorator"
      self."pytest"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/validators";
        license = licenses.bsdOriginal;
        description = "Python Data Validation for Humans™.";
      };
    };



    "waitress" = python.mkDerivation {
      name = "waitress-1.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3c/68/1c10dd5c556872ceebe88483b0436140048d39de83a84a06a8baa8136f4f/waitress-1.1.0.tar.gz"; sha256 = "d33cd3d62426c0f1b3cd84ee3d65779c7003aae3fc060dee60524d10a57f05a9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/Pylons/waitress";
        license = licenses.zpl21;
        description = "Waitress WSGI server";
      };
    };



    "wcwidth" = python.mkDerivation {
      name = "wcwidth-0.1.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/55/11/e4a2bb08bb450fdbd42cc709dd40de4ed2c472cf0ccb9e64af22279c5495/wcwidth-0.1.7.tar.gz"; sha256 = "3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jquast/wcwidth";
        license = licenses.mit;
        description = "Measures number of Terminal column cells of wide-character codes";
      };
    };

  };
  localOverridesFile = ./requirements_override.nix;
  overrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [

  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [overrides] else [] ) ++ commonOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )