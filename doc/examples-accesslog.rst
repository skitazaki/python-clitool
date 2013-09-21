Examples to Parse AccessLog
============================

Create Simple Summary
-------------------------

.. literalinclude:: ../src/logfile.py

Usage
`````

.. code-block:: bash

    $ ./logfile /path/to/access_log

.. csv-table:: Output example
   :header: "Path", "Day", "Hour", "Count"
   :widths: 30, 15, 10, 10
   :stub-columns: 1

    \*,2011-01-30,9,1
    /,2012-10-17,19,2
    /robots.txt,2012-10-17,19,1
    /MyAdmin/scripts/setup.php,2012-10-17,21,1
    /favicon.ico,2012-10-17,21,1
    /myadmin/scripts/setup.php,2012-10-17,21,1
    /phpmyadmin/scripts/setup.php,2012-10-17,21,1
    /pma/scripts/setup.php,2012-10-17,21,1
    /search,2012-10-21,17,1
    /,2012-10-23,16,2
    /,2012-11-05,21,1

Parse Parameters of Each Line
-------------------------------

.. literalinclude:: ../src/logparams.py

Usage
`````

.. code-block:: bash

    $ ./logparams /path/to/access_log


