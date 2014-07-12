# -*- coding: utf-8 -*-

"""
===================================
Command Line Tool Utilities
===================================

* One line argument parsing function and decorator
* Simple configuration loader
* Stream utility with some logging
* CSV reader/writer unicode support for Python 2.x (in official document)
* Apache accesslog parser

Requirements
============

* Python 2.7 or 3.x

Python 2.4, 2.5, 2.6 are not supported.

Install
=======

Use ``pip`` via PyPI.

::

    pip install clitool

Bootstrap
=========

At first, create your script file using module script, ``clitool.cli``.

::

    $ python -m clitool.cli -o your-script.py

This file can parse basic command line options and arguments.

::

    $ ./your-script.py --help
    usage: your-script.py [-h] [-c FILE] [-o FILE] [--basedir BASEDIR]
                          [--input-encoding INPUT_ENCODING]
                          [--output-encoding OUTPUT_ENCODING]
                          [--processes PROCESSES] [--chunksize CHUNKSIZE]
                          [-v | -q]
                          [FILE [FILE ...]]

    positional arguments:
      FILE

    optional arguments:
      -h, --help            show this help message and exit
      -c FILE, --config FILE
                            configuration file
      -o FILE, --output FILE
                            output file
      --basedir BASEDIR     base directory
      --input-encoding INPUT_ENCODING
                            encoding of input source
      --output-encoding OUTPUT_ENCODING
                            encoding of output distination
      --processes PROCESSES
                            count of processes
      --chunksize CHUNKSIZE
                            a number of chunks submitted to the process pool
      -v, --verbose         set logging to verbose mode
      -q, --quiet           set logging to quiet mode

Edit this script on your own :D

Examples
========

Example scripts exist in git repository.

* csv2db.py: read csv data and import database via 'SQLAlchemy'.
* csv2gexf.py: read csv data and dump them by GEXF format via 'NetworkX'.
* csv2json.py: read csv data and dump them by JSON format.
* csv2kml.py: read csv data and dump them by KML format via 'simplekml'.
* logfile.py: parse Apache access log and create report.
* logparams.py: parse Apache access log and analyze query parameters.
"""

__title__ = 'clitool'
__version__ = '0.4.1'
__author__ = 'KITAZAKI Shigeru'

# Constant values.

RUNNING_MODE_ENVKEY = 'PYTHON_CLITOOL_ENV'

DEFAULT_ENCODING = 'utf-8'
DEFAULT_RUNNING_MODE = 'development'

PROCESSING_REPORTING_INTERVAL = 10000
PROCESSING_SUCCESS = 'success'
PROCESSING_SKIPPED = 'skipped'
PROCESSING_ERROR = 'error'
PROCESSING_TOTAL = 'total'
PROCESSING_TIME = 'time'

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
