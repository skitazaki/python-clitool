# -*- coding: utf-8 -*-

"""
Command Line Script Support Utility
===================================

* One line argument parsing function and decorator
* Simple configuration loader
* Stream utility with some logging
* CSV reader/writer unicode support for Python 2.x (in official document)
* Apache accesslog parser

"""

__title__ = 'clitool'
__version__ = '0.3.2'
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
