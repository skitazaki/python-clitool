=========
Examples
=========

Examples to Convert CSV File
============================

CSV to JSON
------------

This script uses following modules.

* ``clitool.cli.climain`` to parse command line options.
* ``clitool.cli.clistream`` to consume input file(s) or standard input.
* ``clitool.textio.Sequential`` to call functions sequentially.
* ``clitool.textio.RowMapper`` to map input row to internal representation.

You can prepare input data from this datapackage.

* https://github.com/skitazaki/datasets-zipcode-jp

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    """Data converting script from CSV to JSON.

    This script accepts Japan Post Code CSV file, a.k.a. "ken_all.csv".
    """

    import logging
    import json

    from clitool.cli import climain, clistream
    from clitool.textio import Sequential, RowMapper

    ENCODING = 'utf-8'

    FIELDS = (
        {"id": "jis_code", "type": "string"},
        {"id": "old_zipcode", "type": "string"},
        {"id": "zipcode", "type": "string"},
        {"id": "prefecture_kana", "type": "string"},
        {"id": "city_kana", "type": "string"},
        {"id": "town_kana", "type": "string"},
        {"id": "prefecture", "type": "string"},
        {"id": "city", "type": "string"},
        {"id": "town", "type": "string"},
        {"id": "multi_zipcode", "type": "boolean"},
        {"id": "koaza_split", "type": "boolean"},
        {"id": "choume_view", "type": "boolean"},
        {"id": "multi_chouiki", "type": "boolean"},
        {"id": "update_view", "type": "integer"},
        {"id": "update_reason", "type": "integer"}
    )


    @climain
    def main(files, output):
        if len(files) > 1:
            raise SystemExit("Only one file or standard input is acceptable.")

        # Load all data on memory from given csv file
        memory = []
        s = Sequential()
        s.callback(RowMapper(FIELDS))
        s.callback(memory.append)
        s.errback(logging.error)
        clistream(s, files=files, delimiter=',')

        # Dump to given output stream, default is standard output
        json.dump(memory, output, indent=2)


    if __name__ == '__main__':
        main()


CSV to Database
---------------

This script uses following modules.

* ``clitool.cli.climain`` to parse command line options.
* ``clitool.cli.clistream`` to consume input file(s) or standard input.
* ``clitool.cli.cliconfig`` to load configuration along with environmental variable.

*TO BE WRITTEN*
