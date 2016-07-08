# generated using pypi2nix tool (version: 1.2.0)
#
# COMMAND:
#   pypi2nix -V 3.5 -E libffi postgresql -r requirements.txt
#

{ pkgs, python, commonBuildInputs ? [], commonDoCheck ? false }:

self: {

  "Babel" = python.mkDerivation {
    name = "Babel-2.3.4";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/6e/96/ba2a2462ed25ca0e651fb7b66e7080f5315f91425a07ea5b34d7c870c114/Babel-2.3.4.tar.gz";
      sha256= "c535c4403802f6eb38173cd4863e419e2274921a01a8aad8a5b497c131c62875";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."pytz"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Internationalization utilities";
    };
    passthru.top_level = false;
  };



  "Flask" = python.mkDerivation {
    name = "Flask-0.11.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/55/8a/78e165d30f0c8bb5d57c429a30ee5749825ed461ad6c959688872643ffb3/Flask-0.11.1.tar.gz";
      sha256= "b4713f2bfb9ebc2966b8a49903ae0d3984781d5c878591cf2f7b484d28756b0e";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Jinja2"
      self."Werkzeug"
      self."click"
      self."itsdangerous"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "A microframework based on Werkzeug, Jinja2 and good intentions";
    };
    passthru.top_level = false;
  };



  "Flask-Admin" = python.mkDerivation {
    name = "Flask-Admin-1.4.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/74/23/a411ce6bca79f30698fbe1d1a59c4789919bdb93fb5385bb24ea07ea7674/Flask-Admin-1.4.2.tar.gz";
      sha256= "7d1cfdcb29a7135d4275dc22628c0f068cccfdb84dadad885bde685d0511597c";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
      self."WTForms"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Simple and extensible admin interface framework for Flask";
    };
    passthru.top_level = false;
  };



  "Flask-BabelEx" = python.mkDerivation {
    name = "Flask-BabelEx-0.9.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/80/ad/cc2b0becd98050eed775ca85d6e5fa784547acff69f968183098df8a52b3/Flask-BabelEx-0.9.3.tar.gz";
      sha256= "cf79cdedb5ce860166120136b0e059e9d97b8df07a3bc2411f6243de04b754b4";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Babel"
      self."Flask"
      self."Jinja2"
      self."speaklater"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Adds i18n/l10n support to Flask applications";
    };
    passthru.top_level = false;
  };



  "Flask-Dance" = python.mkDerivation {
    name = "Flask-Dance-0.9.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/dd/70/991ed825cbc741ce684ca599fef8408916c746a90667d7eb259aba48dac3/Flask-Dance-0.9.0.tar.gz";
      sha256= "36a75a4e15c379673773e677f4c77491b2cf23d7d48b18ad84a52be3e2eceae6";
    };
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
      homepage = "";
      license = licenses.mit;
      description = "Doing the OAuth dance with style using Flask, requests, and oauthlib";
    };
    passthru.top_level = false;
  };



  "Flask-Login" = python.mkDerivation {
    name = "Flask-Login-0.3.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/06/e6/61ed90ed8ce6752b745ed13fac3ba407dc9db95dfa2906edc8dd55dde454/Flask-Login-0.3.2.tar.gz";
      sha256= "e72eff5c35e5a31db1aeca1db5d2501be702674ea88e8f223b5d2b11644beee6";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "User session management for Flask";
    };
    passthru.top_level = false;
  };



  "Flask-Misaka" = python.mkDerivation {
    name = "Flask-Misaka-0.4.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/3d/19/71e8dc5c537f6a4e3b9ae2836f442a8643c2ce900eafd2484ef18ad87cb3/Flask-Misaka-0.4.1.tar.gz";
      sha256= "1dad09a312aafc3783dd4228bcc60708e339494c1653d6bb8e1936b5c4fdeaac";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
      self."misaka"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "A pleasant interface between the Flask web framework and the Misaka Markdown parser.";
    };
    passthru.top_level = false;
  };



  "Flask-SQLAlchemy" = python.mkDerivation {
    name = "Flask-SQLAlchemy-2.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b3/52/227aaf4e8cebb153e239c518a9e916590b2fe0e4350e6b02d92b546b69b7/Flask-SQLAlchemy-2.1.tar.gz";
      sha256= "c5244de44cc85d2267115624d83faef3f9e8f088756788694f305a5d5ad137c5";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
      self."SQLAlchemy"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Adds SQLAlchemy support to your Flask application";
    };
    passthru.top_level = false;
  };



  "Flask-Sijax" = python.mkDerivation {
    name = "Flask-Sijax-0.4.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/97/0e/b2c803d8af324c7161608339496b7a8b05af4711d3da329f8e8d7fc7c49d/Flask-Sijax-0.4.1.tar.gz";
      sha256= "fb2bf2d4f75408185102195055d75549fee8d9c9e954dca2427186925cdc429f";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
      self."Sijax"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "An extension for the Flask microframework that adds Sijax support.";
    };
    passthru.top_level = false;
  };



  "Flask-WTF" = python.mkDerivation {
    name = "Flask-WTF-0.12";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/f6/fe/9fe6a8a4edcc39f8ec365dc16d292d659f7a77a0ed596947f29c0c5c9dc1/Flask-WTF-0.12.tar.gz";
      sha256= "bd99316c97ed1d1cb90b8f0c242c86420a891a6a2058f20717e424bf5b0bb80e";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Flask"
      self."WTForms"
      self."Werkzeug"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Simple integration of Flask and WTForms";
    };
    passthru.top_level = false;
  };



  "Jinja2" = python.mkDerivation {
    name = "Jinja2-2.8";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/f2/2f/0b98b06a345a761bec91a079ccae392d282690c2d8272e708f4d10829e22/Jinja2-2.8.tar.gz";
      sha256= "bc1ff2ff88dbfacefde4ddde471d1417d3b304e8df103a7a9437d47269201bf4";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Babel"
      self."MarkupSafe"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "A small but fast and easy to use stand-alone template engine written in pure python.";
    };
    passthru.top_level = false;
  };



  "MarkupSafe" = python.mkDerivation {
    name = "MarkupSafe-0.23";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/c0/41/bae1254e0396c0cc8cf1751cb7d9afc90a602353695af5952530482c963f/MarkupSafe-0.23.tar.gz";
      sha256= "a4ec1aff59b95a14b45eb2e23761a0179e98319da5a7eb76b56ea8cdc7b871c3";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Implements a XML/HTML/XHTML Markup safe string for Python";
    };
    passthru.top_level = false;
  };



  "PyYAML" = python.mkDerivation {
    name = "PyYAML-3.11";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/75/5e/b84feba55e20f8da46ead76f14a3943c8cb722d40360702b2365b91dec00/PyYAML-3.11.tar.gz";
      sha256= "c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "YAML parser and emitter for Python";
    };
    passthru.top_level = false;
  };



  "Pygments" = python.mkDerivation {
    name = "Pygments-2.1.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b8/67/ab177979be1c81bc99c8d0592ef22d547e70bb4c6815c383286ed5dec504/Pygments-2.1.3.tar.gz";
      sha256= "88e4c8a91b2af5962bfa5ea2447ec6dd357018e86e94c7d14bd8cacbc5b55d81";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Pygments is a syntax highlighting package written in Python.";
    };
    passthru.top_level = false;
  };



  "SQLAlchemy" = python.mkDerivation {
    name = "SQLAlchemy-1.0.14";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/aa/cb/e3990b9da48facbe48b80a281a51fb925ff84aaaca44d368d658b0160fcf/SQLAlchemy-1.0.14.tar.gz";
      sha256= "da4d1a39c1e99c7fecc2aaa3a050094b6aa7134de7d89f77e6216e7abd1705b3";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Database Abstraction Library";
    };
    passthru.top_level = false;
  };



  "SQLAlchemy-Searchable" = python.mkDerivation {
    name = "SQLAlchemy-Searchable-0.10.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b7/c8/5b52eaf5303b1f22ca2dd41ff38f942a3dc0f2d2d239a482868fc8ecf68b/SQLAlchemy-Searchable-0.10.1.tar.gz";
      sha256= "42ab4e04a7e64ce7098807e0e4fc0a21c6e92f26fc9e5415a0491601c756c096";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."SQLAlchemy"
      self."SQLAlchemy-Utils"
      self."psycopg2"
      self."pyparsing"
      self."validators"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Provides fulltext search capabilities for declarative SQLAlchemy models.";
    };
    passthru.top_level = false;
  };



  "SQLAlchemy-Utils" = python.mkDerivation {
    name = "SQLAlchemy-Utils-0.32.7";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/cd/f3/f4399406309b9b37305bcadec371f417573aea16a2bf9990e0e8176a45ae/SQLAlchemy-Utils-0.32.7.tar.gz";
      sha256= "ef4dcddee21114257b8384adc5746556a5d815a2e3aec66beaa78aeaf5e695e7";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Babel"
      self."Jinja2"
      self."Pygments"
      self."SQLAlchemy"
      self."psycopg2"
      self."pytz"
      self."six"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Various utility functions for SQLAlchemy.";
    };
    passthru.top_level = false;
  };



  "Sijax" = python.mkDerivation {
    name = "Sijax-0.3.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/3a/08/32c4e77caafc7542195cfb00e0ee400f1d9e29c4259842c3b32441b39bd3/Sijax-0.3.2.tar.gz";
      sha256= "11b062f4a8b2aad95c87e7c09e5daf5a6b0d0f08abf9efe5f91a0075c6be7c0d";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."future"
      self."six"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "An easy to use AJAX library based on jQuery.ajax";
    };
    passthru.top_level = false;
  };



  "URLObject" = python.mkDerivation {
    name = "URLObject-2.4.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/cb/b6/e25e58500f9caef85d664bec71ec67c116897bfebf8622c32cb75d1ca199/URLObject-2.4.0.tar.gz";
      sha256= "f51272b12846db98af530b0a64f6593d2b1e8405f0aa580285b37ce8009b8d9c";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "A utility class for manipulating URLs.";
    };
    passthru.top_level = false;
  };



  "WTForms" = python.mkDerivation {
    name = "WTForms-2.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/bf/91/2e553b86c55e9cf2f33265de50e052441fb753af46f5f20477fe9c61280e/WTForms-2.1.zip";
      sha256= "ffdf10bd1fa565b8233380cb77a304cd36fd55c73023e91d4b803c96bc11d46f";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Babel"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "A flexible forms validation and rendering library for python web development.";
    };
    passthru.top_level = false;
  };



  "Werkzeug" = python.mkDerivation {
    name = "Werkzeug-0.11.10";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b7/7f/44d3cfe5a12ba002b253f6985a4477edfa66da53787a2a838a40f6415263/Werkzeug-0.11.10.tar.gz";
      sha256= "cc64dafbacc716cdd42503cf6c44cb5a35576443d82f29f6829e5c49264aeeee";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "The Swiss Army knife of Python web development";
    };
    passthru.top_level = false;
  };



  "blinker" = python.mkDerivation {
    name = "blinker-1.4";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/1b/51/e2a9f3b757eb802f61dc1f2b09c8c99f6eb01cf06416c0671253536517b6/blinker-1.4.tar.gz";
      sha256= "471aee25f3992bd325afa3772f1063dbdbbca947a041b8b89466dc00d606f8b6";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Fast, simple object-to-object and broadcast signaling";
    };
    passthru.top_level = false;
  };



  "cffi" = python.mkDerivation {
    name = "cffi-1.7.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/83/3c/00b553fd05ae32f27b3637f705c413c4ce71290aa9b4c4764df694e906d9/cffi-1.7.0.tar.gz";
      sha256= "6ed5dd6afd8361f34819c68aaebf9e8fc12b5a5893f91f50c9e50c8886bb60df";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."pycparser"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Foreign Function Interface for Python calling C code.";
    };
    passthru.top_level = false;
  };



  "click" = python.mkDerivation {
    name = "click-6.6";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/7a/00/c14926d8232b36b08218067bcd5853caefb4737cda3f0a47437151344792/click-6.6.tar.gz";
      sha256= "cc6a19da8ebff6e7074f731447ef7e112bd23adf3de5c597cf9989f2fd8defe9";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "A simple wrapper around optparse for powerful command line utilities.";
    };
    passthru.top_level = false;
  };



  "decorator" = python.mkDerivation {
    name = "decorator-4.0.10";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/13/8a/4eed41e338e8dcc13ca41c94b142d4d20c0de684ee5065523fee406ce76f/decorator-4.0.10.tar.gz";
      sha256= "9c6e98edcb33499881b86ede07d9968c81ab7c769e28e9af24075f0a5379f070";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "new BSD License";
      description = "Better living through Python with decorators";
    };
    passthru.top_level = false;
  };



  "future" = python.mkDerivation {
    name = "future-0.15.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/5a/f4/99abde815842bc6e97d5a7806ad51236630da14ca2f3b1fce94c0bb94d3d/future-0.15.2.tar.gz";
      sha256= "3d3b193f20ca62ba7d8782589922878820d0a023b885882deec830adbf639b97";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Clean single-source support for Python 3 and 2";
    };
    passthru.top_level = false;
  };



  "ipython" = python.mkDerivation {
    name = "ipython-5.0.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/09/2e/870d1058768f5240062beb0bd2ff789ac689923501b0dd6b480fb83314fc/ipython-5.0.0.tar.gz";
      sha256= "7ec0737169c74056c7fc8298246db5478a2d6c90cfd19c3253222112357545df";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."Pygments"
      self."decorator"
      self."pexpect"
      self."pickleshare"
      self."prompt-toolkit"
      self."requests"
      self."simplegeneric"
      self."traitlets"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "IPython: Productive Interactive Computing";
    };
    passthru.top_level = false;
  };



  "ipython-genutils" = python.mkDerivation {
    name = "ipython-genutils-0.1.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/71/b7/a64c71578521606edbbce15151358598f3dfb72a3431763edc2baf19e71f/ipython_genutils-0.1.0.tar.gz";
      sha256= "3a0624a251a26463c9dfa0ffa635ec51c4265380980d9a50d65611c3c2bd82a6";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Vestigial utilities from IPython";
    };
    passthru.top_level = false;
  };



  "itsdangerous" = python.mkDerivation {
    name = "itsdangerous-0.24";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz";
      sha256= "cbb3fcf8d3e33df861709ecaf89d9e6629cff0a217bc2848f1b41cd30d360519";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "Various helpers to pass trusted data to untrusted environments and back.";
    };
    passthru.top_level = false;
  };



  "lazy" = python.mkDerivation {
    name = "lazy-1.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/01/09/45e590953c798349f2b5b2d2c2d669bd2b909e254d75f4f70e55cde8edae/lazy-1.2.zip";
      sha256= "127ea610418057b953f0d102bed83f2c367be13b59f8d0ddf3b8a86c7d31b970";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Lazy attributes for Python objects";
    };
    passthru.top_level = false;
  };



  "misaka" = python.mkDerivation {
    name = "misaka-2.0.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/10/38/a2f575ae8552b15d20b0ce3f5f5e60052091069c42ad07462fe3027f8f0d/misaka-2.0.0.tar.gz";
      sha256= "336ef1381ab840046b7da9f95c4c28af17e636aed8dcfcf1efe972db05f73604";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."cffi"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "A CFFI binding for Hoedown, a markdown parsing library.";
    };
    passthru.top_level = false;
  };



  "oauthlib" = python.mkDerivation {
    name = "oauthlib-1.1.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/a8/11/fb71ced7057b2a8929f51959f4e97bcee9f687aaf896c521984e67118b90/oauthlib-1.1.2.tar.gz";
      sha256= "0e83e91d9e77a396dc178eddba0c4abf75e465761804bfcdb20b977284bcb0bb";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."blinker"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "A generic, spec-compliant, thorough implementation of the OAuth request-signing logic";
    };
    passthru.top_level = false;
  };



  "pexpect" = python.mkDerivation {
    name = "pexpect-4.2.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b3/7b/7b3659b9d7059d6d21e23b2464c5c84bffd4a34450cbf0ed19c9a8a4a52f/pexpect-4.2.0.tar.gz";
      sha256= "bf6816b8cc8d301a499e7adf338828b39bc7548eb64dbed4dd410ed93d95f853";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."ptyprocess"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "ISC license";
      description = "Pexpect allows easy control of interactive console applications.";
    };
    passthru.top_level = false;
  };



  "pickleshare" = python.mkDerivation {
    name = "pickleshare-0.7.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/ad/69/bcf0c55ded3779e6e1c9460c69854678d4b78f08482449caaf8e82d5f8eb/pickleshare-0.7.2.tar.gz";
      sha256= "92ee3b0e21632542ecc9a0a245e69a126f62e5114081bdb0d32e0edd10410033";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Tiny 'shelve'-like database with concurrency support";
    };
    passthru.top_level = false;
  };



  "prompt-toolkit" = python.mkDerivation {
    name = "prompt-toolkit-1.0.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/8d/de/412f23919929c01e6b55183e124623f705e4b91796d3d2dce2cb53d595ad/prompt_toolkit-1.0.3.tar.gz";
      sha256= "805e026f0cbad27467e93f9dd3e3777718d401a62788c1e84ca038e967ad8ba2";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."six"
      self."wcwidth"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "Library for building powerful interactive command lines in Python";
    };
    passthru.top_level = false;
  };



  "psycopg2" = python.mkDerivation {
    name = "psycopg2-2.6.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/7b/a8/dc2d50a6f37c157459cd18bab381c8e6134b9381b50fbe969997b2ae7dbc/psycopg2-2.6.2.tar.gz";
      sha256= "70490e12ed9c5c818ecd85d185d363335cc8a8cbf7212e3c185431c79ff8c05c";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "LGPL with exceptions or ZPL";
      description = "psycopg2 - Python-PostgreSQL Database Adapter";
    };
    passthru.top_level = false;
  };



  "ptyprocess" = python.mkDerivation {
    name = "ptyprocess-0.5.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/db/d7/b465161910f3d1cef593c5e002bff67e0384898f597f1a7fdc8db4c02bf6/ptyprocess-0.5.1.tar.gz";
      sha256= "0530ce63a9295bfae7bd06edc02b6aa935619f486f0f1dc0972f516265ee81a6";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "Run a subprocess in a pseudo terminal";
    };
    passthru.top_level = false;
  };



  "pycparser" = python.mkDerivation {
    name = "pycparser-2.14";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/6d/31/666614af3db0acf377876d48688c5d334b6e493b96d21aa7d332169bee50/pycparser-2.14.tar.gz";
      sha256= "7959b4a74abdc27b312fed1c21e6caf9309ce0b29ea86b591fd2e99ecdf27f73";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "C parser in Python";
    };
    passthru.top_level = false;
  };



  "pyjade" = python.mkDerivation {
    name = "pyjade-4.0.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/4a/04/396ec24e806fd3af7ea5d0f3cb6c7bbd4d00f7064712e4dd48f24c02ca95/pyjade-4.0.0.tar.gz";
      sha256= "8d95b741de09c4942259fc3d1ad7b4f48166e69cef6f11c172e4b2c458b1ccd7";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."six"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Jade syntax template adapter for Django, Jinja2, Mako and Tornado templates";
    };
    passthru.top_level = false;
  };



  "pyparsing" = python.mkDerivation {
    name = "pyparsing-2.1.5";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/30/c3/a424fb888af373b54df495a0582379df374322caabd4f3a549bcca72aeeb/pyparsing-2.1.5.tar.gz";
      sha256= "b9ace99b581174d7ca98891a7bc57fd08892b94f17922645d90835f7b9b54a56";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Python parsing module";
    };
    passthru.top_level = false;
  };



  "pytz" = python.mkDerivation {
    name = "pytz-2016.4";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/f4/7d/7c0c85e9c64a75dde11bc9d3e1adc4e09a42ce7cdb873baffa1598118709/pytz-2016.4.tar.bz2";
      sha256= "ee7c751544e35a7b7fb5e3fb25a49dade37d51e70a93e5107f10575d7102c311";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "World timezone definitions, modern and historical";
    };
    passthru.top_level = false;
  };



  "requests" = python.mkDerivation {
    name = "requests-2.10.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/49/6f/183063f01aae1e025cf0130772b55848750a2f3a89bfa11b385b35d7329d/requests-2.10.0.tar.gz";
      sha256= "63f1815788157130cee16a933b2ee184038e975f0017306d723ac326b5525b54";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.asl20;
      description = "Python HTTP for Humans.";
    };
    passthru.top_level = false;
  };



  "requests-oauthlib" = python.mkDerivation {
    name = "requests-oauthlib-0.6.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/f9/98/a1aaae4bbcde0e98d6d853c4f08bd52f20b0005cefb881679bcdf7ea7a00/requests-oauthlib-0.6.1.tar.gz";
      sha256= "905306080ec0cc6b3c65c8101f471fccfdb9994c16dd116524fd3fc0790d46d7";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."oauthlib"
      self."requests"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "ISC";
      description = "OAuthlib authentication support for Requests.";
    };
    passthru.top_level = false;
  };



  "simplegeneric" = python.mkDerivation {
    name = "simplegeneric-0.8.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/3d/57/4d9c9e3ae9a255cd4e1106bb57e24056d3d0709fc01b2e3e345898e49d5b/simplegeneric-0.8.1.zip";
      sha256= "dc972e06094b9af5b855b3df4a646395e43d1c9d0d39ed345b7393560d0b9173";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.zpt21;
      description = "Simple generic functions (similar to Python's own len(), pickle.dump(), etc.)";
    };
    passthru.top_level = false;
  };



  "six" = python.mkDerivation {
    name = "six-1.10.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz";
      sha256= "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Python 2 and 3 compatibility utilities";
    };
    passthru.top_level = false;
  };



  "speaklater" = python.mkDerivation {
    name = "speaklater-1.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/11/92/5ae1effe0ccb8561c034a0111d53c8788660ddb7ed4992f0da1bb5c525e5/speaklater-1.3.tar.gz";
      sha256= "59fea336d0eed38c1f0bf3181ee1222d0ef45f3a9dd34ebe65e6bfffdd6a65a9";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = "";
      description = "implements a lazy string for python useful for use with gettext";
    };
    passthru.top_level = false;
  };



  "traitlets" = python.mkDerivation {
    name = "traitlets-4.2.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/a4/07/9b7636322c152ab1dacae9d38131067523d6ce5ca926a656586f6f947e77/traitlets-4.2.2.tar.gz";
      sha256= "7d7e3070484b2fe490fa55e0acf7023afc5ed9ddabec57405f25c355158e152a";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."decorator"
      self."ipython-genutils"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Traitlets Python config system";
    };
    passthru.top_level = false;
  };



  "validators" = python.mkDerivation {
    name = "validators-0.10.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/70/fe/ea5ded687563c6ce88aa72472bfce98ed2f49915d438cb18bd4d55b8c532/validators-0.10.3.tar.gz";
      sha256= "2681da24537498dcc54ee759c6458b713df87aba6bf217c9fbcbe7bf671e42c8";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [
      self."decorator"
      self."six"
    ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.bsdOriginal;
      description = "Python Data Validation for Humans™.";
    };
    passthru.top_level = false;
  };



  "wcwidth" = python.mkDerivation {
    name = "wcwidth-0.1.7";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/55/11/e4a2bb08bb450fdbd42cc709dd40de4ed2c472cf0ccb9e64af22279c5495/wcwidth-0.1.7.tar.gz";
      sha256= "3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e";
    };
    doCheck = commonDoCheck;
    buildInputs = commonBuildInputs;
    propagatedBuildInputs = [ ];
    meta = with pkgs.stdenv.lib; {
      homepage = "";
      license = licenses.mit;
      description = "Measures number of Terminal column cells of wide-character codes";
    };
    passthru.top_level = false;
  };

}