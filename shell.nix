{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python310Packages; [
    ipython
    jupyter
    jupyterlab
    matplotlib
    pandas
    plotly
    numpy
    rich
    appdirs
    async-timeout
    attrs
    cattrs
    certifi
    cffi
    charset-normalizer
    click
    cycler
    # Deprecated
    distlib
    filelock
    flask
    flask-cors
    flask-httpauth
    fonttools
    # frozen-flask
    gunicorn
    idna
    iniconfig
    itsdangerous
    jinja2
    kiwisolver
    markupsafe
    matplotlib
    numpy
    packaging
    pandas
    pillow
    platformdirs
    plotly
    pluggy
    py
    pycparser
    PyGithub
    pyparsing
    pytest
    python-dateutil
    python-dotenv
    pytz
    redis
    requests
    requests-cache
    scipy
    seaborn
    simplejson
    six
    tenacity
    tinydb
    tomli
    url-normalize
    urllib3
    virtualenv
  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
