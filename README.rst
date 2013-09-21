==================================
Command line tool project template
==================================

[master]

.. image:: https://secure.travis-ci.org/skitazaki/python-clitool-template.png?branch=master
    :target: https://secure.travis-ci.org/skitazaki/python-clitool-template

[develop]

.. image:: https://secure.travis-ci.org/skitazaki/python-clitool-template.png?branch=develop
    :target: https://secure.travis-ci.org/skitazaki/python-clitool-template

Prerequisites
=============

* Python 2.7
* virtualenv + pip

or

* Python 3.x
* (virtualenv or pyvenv) + pip

Setup
=====

Python 2.7
----------

Create working directoty and activate it.

::

    $ virtualenv --distribute ~/pyvenv2/clitool
    $ source ~/pyvenv2/clitool/bin/activate

Install build tool, ``waf``.

::

    $ ln -s `pwd`/etc/waf-1.7.9 ~/pyvenv2/clitool/bin/waf

Install dependant libraries.

::

    $ pip install -r requirements.txt
    $ pip install python-dateutil==1.5 pyflakes

Python 3.3
----------

Create working directoty and activate it.

::

    $ pyvenv ~/pyvenv3/clitool
    $ source ~/pyvenv3/clitool/bin/activate

Install build tool, ``waf``.

::

    $ ln -s `pwd`/etc/waf-1.7.9 ~/pyvenv3/clitool/bin/waf

Install ``pip`` and dependant libraries.

::

    $ pip-3.3 install -r requirements.txt
    $ pip-3.3 install python-dateutil>=2.0

Check installation
------------------

Check required tools are successfully installed.

::

    $ waf configure

Build & Release
===============

``cleanbuild`` target includes ``distclean``, ``configure``, ``build``, ``test``, and ``example``.

::

    $ waf cleanbuild

To relase on PyPI, use ``release`` target.
Don't forget to check test result on travis-ci.

::

    $ waf release

To create API documentation, use ``apidoc`` target.

::

    $ waf apidoc

And upload generated ZIP file on PyPI manually.

Project layout
==============

* *doc*   : Specification or API documentations.
* *etc*   : Support files, such as win32 specific scripts.
* *src*   : Main source code go here.
* *tests* : Test code go here.
* *data*  : Various data files for test.

Copyright and license
======================

Copyright 2013 Shigeru Kitazaki

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
