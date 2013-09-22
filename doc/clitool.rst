:mod:`clitool` Package
======================

:mod:`cli` Module
-----------------


This module provides three features:

1. :func:`climain` decorator for main function to parse basic command line options.
2. :func:`~clitool.cli.cliconfig` to load configuration file with multiple environments.
3. :func:`~clitool.cli.clistream` to handle files or standard input as command line arguments.

Basic script looks like::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from pprint import pprint

    from clitool.cli import climain, cliconfig, clistream


    @climain
    def main(config, output, **kwargs):
        # Load all tab-separated data onto `data`.
        data = []
        clistream(data.append, delimiter='\t', **kwargs)

        # Dump all data into given output stream. (default is standard output)
        pprint(data, stream=output)

        # Get database connection from given configuration file.
        cfg = cliconfig(config)
        dsl = cfg.get("YOUR_DATABASE_CONFIG_KEY")
        # Implement database session factory code.
        session = SessionFactory(dsl).create()

        # Save all data on database
        for dt = data:
            # Implement mapping code from input to database model.
            e = mapping(dt)
            session.save(e)

        session.commit()


    if __name__ == '__main__':
        main()

.. py:decorator:: climain

    Decorator for main function to parse basic command line options and arguments.
    This is a simple wrapper of :func:`~clitool.cli.parse_arguments` expecting
    multiple files as command line argument, and passes command line options and
    arguments to wrapping function.

    The wrapped function get keyword arguments defined in
    :func:`~clitool.cli.base_parser` and `files` which you can ignore.
    The sequence is on your own.

    A example which accepts multiple input files, one output file-like object,
    input/output encoding, and other keywords is such like:

    .. code-block:: python

        from clitool.cli import climain

        @climain
        def main(files, input_encoding, output, output_encoding, **kwargs):
            # your main function goes here
            if files:
                print("Hello %d inputs with %s." % (len(files), input_encoding))

.. automodule:: clitool.cli
    :members:
    :show-inheritance:


:mod:`config` Module
--------------------

.. automodule:: clitool.config
    :members:
    :undoc-members:
    :show-inheritance:

Configuration file examples
```````````````````````````

INI format

.. code-block:: ini

    [development]
    database.url=sqlite:///sample.sqlite

    [staging]
    database.url=postgresql+pypostgresql://user:pass@host/database

    [production]
    database.url=mysql://user:pass@host/database

JSON style

.. code-block:: json

    {
        "development": {
            "database": {
                "url": "sqlite:///sample.sqlite"
            }
        },
        "staging": {
            "database": {
                "url": "postgresql+pypostgresql://user:pass@host/database"
            }
        },
        "production": {
            "database": {
                "url": "mysql+mysqlconnector://user:pass@host/database"
            }
        }
    }

YAML style

.. code-block:: yaml

    development:
      database:
        url: "sqlite:///sample.sqlite"

    staging:
      database:
        url: "postgresql+pypostgresql://user:pass@host/database"

    production:
      database:
        url: "mysql://user:pass@host/database"

:mod:`processor` Module
-----------------------

.. automodule:: clitool.processor
    :members:
    :show-inheritance:

:mod:`accesslog` Module
-----------------------

.. automodule:: clitool.accesslog
    :members:
    :undoc-members:
    :show-inheritance:

Parsed record is a map object which has following properties.

- *host* : Remote IP address.
- *time* : Access date and time. (datetime object)
- *path* : HTTP request path which is splitted from query.
- *query* : HTTP requert query string which is removed from "?".
- *method* : HTTP request method.
- *protocol* : HTTP request protocol version.
- *status* : HTTP response status code. (int)
- *size* : HTTP response size, if available. (int)
- *referer* : Referer header. If "-" is given, this property does not exist.
- *ua* : User agent. If "-" is given, this property does not exist.
- *ident* : remote logname
- *user* : remote user
- *trailing* : Additional information if using custom log format.

This module also work as script file.
Simple usage is that:

.. code-block:: bash

    $ tail -f /var/log/httpd/access_log | python -m clitool.accesslog

And two options are available.

- *--color* : Set color on error record.
- *--status* : Filter condition along with response status.

If you would like to check only error responses, set ``--status=500,503``.

Since the script expand each record on key/value manner, you can combine it
with ``grep`` or any other Unix-like tools.
To get Top 10 access, try it.

.. code-block:: bash

    $ python -m clitool.accesslog /var/log/httpd/access_log |
        grep request_path | sort | uniq -c | sort -nr | head -n 10

:mod:`textio` Module
-----------------------

.. automodule:: clitool.textio
    :members:
    :show-inheritance:


:mod:`_unicodecsv` Module
-------------------------

.. automodule:: clitool._unicodecsv
    :members:
    :undoc-members:
    :show-inheritance:

