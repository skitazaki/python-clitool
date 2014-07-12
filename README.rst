==================================
Command Line Tool Utilities
==================================

[master]

.. image:: https://secure.travis-ci.org/skitazaki/python-clitool.png?branch=master
    :target: https://secure.travis-ci.org/skitazaki/python-clitool

[develop]

.. image:: https://secure.travis-ci.org/skitazaki/python-clitool.png?branch=develop
    :target: https://secure.travis-ci.org/skitazaki/python-clitool

Prerequisites
=============

* Python 2.7
* virtualenv + pip

or

* Python 3.4

Development Setup
==================

Python 2.7
----------

Create working directoty and activate it.

::

    $ virtualenv --distribute ~/.pyvenv/python-clitool-py27
    $ source ~/.pyvenv/python-clitool-py27/bin/activate

Install build tool, ``waf``.

::

    $ ln -s `pwd`/etc/waf-1.7.13 ~/.pyvenv/python-clitool-py27/bin/waf

Install dependant libraries.

::

    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt
    $ pip install pyflakes

Python 3.4
----------

Create working directoty and activate it.

::

    $ pyvenv ~/.pyvenv/python-clitool-py34
    $ source ~/.pyvenv/python-clitool-py34/bin/activate

Install build tool, ``waf``.

::

    $ ln -s `pwd`/etc/waf-1.7.13 ~/.pyvenv/python-clitool-py34/bin/waf

Install dependant libraries.

::

    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt

Check installation
------------------

Check required tools are successfully installed.

::

    $ waf configure

Build & Release
===============

``cleanbuild`` target includes ``distclean``, ``configure``, ``build``, and ``example``.

::

    $ waf cleanbuild

To relase on PyPI, use ``release`` target.
Don't forget to check test result on travis-ci.

::

    $ waf release

And, forget to upload generated ZIP file of documents on PyPI manually.

Project layout
==============

* *clitool* : Main source code go here.
* *doc*     : Specification or API documentations.
* *etc*     : Support files
* *tests*   : Test code go here.

Copyright and license
======================

Copyright 2014 Shigeru Kitazaki

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

