.. clitool documentation master file, created by
   sphinx-quickstart on Thu Nov  8 00:56:18 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to clitool's documentation!
===================================

`clitool` is a handy library to support you implementing command line script.
This library cuts off redundant argument parsing and configuration loading,
and also provides a feature to handle streaming data with some logging.

You can try a simple solution to parse Apache accesslog and create key/value
report. This will be suitable for Hadoop Streaming environment.

List of features are:

* One line argument parsing function and decorator
* Simple configuration loader
* Stream utility with some logging
* CSV reader/writer unicode support for Python 2.x (in official document)
* Apache accesslog parser

Contents:

.. toctree::
   :maxdepth: 2

   examples-csv
   examples-accesslog
   examples-misc
   clitool
