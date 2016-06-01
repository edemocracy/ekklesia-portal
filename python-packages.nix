{
  Babel = super.buildPythonPackage {
    name = "Babel-2.2.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [pytz];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/B/Babel/Babel-2.2.0.tar.gz";
      md5 = "1b69e4b2ab3795119266ccaa36b36f15";
    };
  };
  Jinja2 = super.buildPythonPackage {
    name = "Jinja2-2.8";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [MarkupSafe];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.8.tar.gz";
      md5 = "edb51693fe22c53cee5403775c71a99e";
    };
  };
  MarkupSafe = super.buildPythonPackage {
    name = "MarkupSafe-0.23";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.23.tar.gz";
      md5 = "f5ab3deee4c37cd6a922fb81e730da6e";
    };
  };
  SQLAlchemy = super.buildPythonPackage {
    name = "SQLAlchemy-1.0.12";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-1.0.12.tar.gz";
      md5 = "6d19ef29883bbebdcac6613cf391cac4";
    };
  };
  SQLAlchemy-Utils = super.buildPythonPackage {
    name = "SQLAlchemy-Utils-0.32.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [six SQLAlchemy];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/S/SQLAlchemy-Utils/SQLAlchemy-Utils-0.32.0.tar.gz";
      md5 = "ccf82b341312d60f8df86b54e0fcd023";
    };
  };
  Sijax = super.buildPythonPackage {
    name = "Sijax-0.3.2";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [six future];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/S/Sijax/Sijax-0.3.2.tar.gz";
      md5 = "0fe4be64bc6f559afe73436f43cbf11f";
    };
  };
  Werkzeug = super.buildPythonPackage {
    name = "Werkzeug-0.11.10";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/b7/7f/44d3cfe5a12ba002b253f6985a4477edfa66da53787a2a838a40f6415263/Werkzeug-0.11.10.tar.gz";
      md5 = "780967186f9157e88f2bfbfa6f07a893";
    };
  };
  blinker = super.buildPythonPackage {
    name = "blinker-1.4";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/b/blinker/blinker-1.4.tar.gz";
      md5 = "8b3722381f83c2813c52de3016b68d33";
    };
  };
  decorator = super.buildPythonPackage {
    name = "decorator-4.0.9";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/decorator/decorator-4.0.9.tar.gz";
      md5 = "f12c5651ccd707e12a0abaa4f76cd69a";
    };
  };
  click = super.buildPythonPackage {
    name = "click-6.6";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/7a/00/c14926d8232b36b08218067bcd5853caefb4737cda3f0a47437151344792/click-6.6.tar.gz";
      md5 = "d0b09582123605220ad6977175f3e51d";
    };
  };
  flask = super.buildPythonPackage {
    name = "flask-0.11";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [Werkzeug Jinja2 itsdangerous click];
    src = fetchurl {
      url = "https://pypi.python.org/packages/dc/ca/c0ed9cc90c079085c698e284b672edbc1ffd6866b1830574095cbc5b7752/Flask-0.11.tar.gz";
      md5 = "89fbdcb04b7b96c5b24625ae299cf48b";
    };
  };
  flask-admin = super.buildPythonPackage {
    name = "flask-admin-1.4.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask wtforms];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-Admin/Flask-Admin-1.4.0.tar.gz";
      md5 = "7b24933924f1de60c7dafc371bcbb6f4";
    };
  };
  flask-babelex = super.buildPythonPackage {
    name = "flask-babelex-0.9.3";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask Babel speaklater Jinja2];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-BabelEx/Flask-BabelEx-0.9.3.tar.gz";
      md5 = "59a0fdc99be059365fd5aa673a429189";
    };
  };
  flask-dance = super.buildPythonPackage {
    name = "flask-dance-0.8.2";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [requests oauthlib requests-oauthlib flask urlobject six lazy];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-Dance/Flask-Dance-0.8.2.tar.gz";
      md5 = "4ad4a421de2742f58f24c88704be94ed";
    };
  };
  flask-login = super.buildPythonPackage {
    name = "flask-login-0.3.2";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-Login/Flask-Login-0.3.2.tar.gz";
      md5 = "d95c2275d3e1c755145910077366dc45";
    };
  };
  flask-sijax = super.buildPythonPackage {
    name = "flask-sijax-0.4.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask Sijax];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-Sijax/Flask-Sijax-0.4.1.tar.gz";
      md5 = "c64f2b0b6eced637042a99a9bf0e507b";
    };
  };
  flask-sqlalchemy = super.buildPythonPackage {
    name = "flask-sqlalchemy-2.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask SQLAlchemy];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-SQLAlchemy/Flask-SQLAlchemy-2.1.tar.gz";
      md5 = "dc15fe08b07b434d3d2c4063b4674b72";
    };
  };
  flask-wtf = super.buildPythonPackage {
    name = "flask-wtf-0.12";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [flask Werkzeug wtforms];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Flask-WTF/Flask-WTF-0.12.tar.gz";
      md5 = "c53a74e8ba481bf53405fd5efdf0339e";
    };
  };
  future = super.buildPythonPackage {
    name = "future-0.15.2";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/f/future/future-0.15.2.tar.gz";
      md5 = "a68eb3c90b3b76714c5ceb8c09ea3a06";
    };
  };
  itsdangerous = super.buildPythonPackage {
    name = "itsdangerous-0.24";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/i/itsdangerous/itsdangerous-0.24.tar.gz";
      md5 = "a3d55aa79369aef5345c036a8a26307f";
    };
  };
  lazy = super.buildPythonPackage {
    name = "lazy-1.2";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/l/lazy/lazy-1.2.zip";
      md5 = "02713784e0a92ff9b6af1df8863dd79d";
    };
  };
  oauthlib = super.buildPythonPackage {
    name = "oauthlib-1.0.3";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/o/oauthlib/oauthlib-1.0.3.tar.gz";
      md5 = "02772867bf246b3b37f4ed22786c41f5";
    };
  };
  psycopg2 = super.buildPythonPackage {
    name = "psycopg2-2.6.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/psycopg2/psycopg2-2.6.1.tar.gz";
      md5 = "842b44f8c95517ed5b792081a2370da1";
    };
  };
  pyjade = super.buildPythonPackage {
    name = "pyjade-4.0.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [six];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/pyjade/pyjade-4.0.0.tar.gz";
      md5 = "c25c8433c0aed7d0e47de4e3f9bc8026";
    };
  };
  pyparsing = super.buildPythonPackage {
    name = "pyparsing-2.1.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/pyparsing/pyparsing-2.1.0.tar.gz";
      md5 = "6fc363eb77331f9cf435d65f63f364ea";
    };
  };
  pytz = super.buildPythonPackage {
    name = "pytz-2016.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/pytz/pytz-2016.1.tar.bz2";
      md5 = "581093ed74ceecfc994e8df82bcbaac5";
    };
  };
  pyyaml = super.buildPythonPackage {
    name = "pyyaml-3.11";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz";
      md5 = "f50e08ef0fe55178479d3a618efe21db";
    };
  };
  requests = super.buildPythonPackage {
    name = "requests-2.9.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/r/requests/requests-2.9.1.tar.gz";
      md5 = "0b7f480d19012ec52bab78292efd976d";
    };
  };
  requests-oauthlib = super.buildPythonPackage {
    name = "requests-oauthlib-0.6.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [oauthlib requests];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/r/requests-oauthlib/requests-oauthlib-0.6.1.tar.gz";
      md5 = "f159bc7675ebe6a2d76798f4c00c5bf8";
    };
  };
  six = super.buildPythonPackage {
    name = "six-1.10.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz";
      md5 = "34eed507548117b2ab523ab14b2f8b55";
    };
  };
  speaklater = super.buildPythonPackage {
    name = "speaklater-1.3";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/s/speaklater/speaklater-1.3.tar.gz";
      md5 = "e8d5dbe36e53d5a35cff227e795e8bbf";
    };
  };
  sqlalchemy-searchable = super.buildPythonPackage {
    name = "sqlalchemy-searchable-0.9.3";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [pyparsing SQLAlchemy SQLAlchemy-Utils validators];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/S/SQLAlchemy-Searchable/SQLAlchemy-Searchable-0.9.3.tar.gz";
      md5 = "fc3e7388484aeb21b4a6b5af208a5544";
    };
  };
  urlobject = super.buildPythonPackage {
    name = "urlobject-2.4.0";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/U/URLObject/URLObject-2.4.0.tar.gz";
      md5 = "2ed819738a9f0a3051f31dc9924e3065";
    };
  };
  validators = super.buildPythonPackage {
    name = "validators-0.10";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [six decorator];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/v/validators/validators-0.10.tar.gz";
      md5 = "9ddd9d77aadc047723080da500e0bbf2";
    };
  };
  wtforms = super.buildPythonPackage {
    name = "wtforms-2.1";
    buildInputs = with self; [];
    doCheck = false;
    propagatedBuildInputs = with self; [];
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/W/WTForms/WTForms-2.1.zip";
      md5 = "6938a541fafd1a1ae2f6b9b88588eef2";
    };
  };

### Test requirements

  
}
