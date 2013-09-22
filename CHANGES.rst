Release 0.4.0 (released Sep 22, 2013)
=========================================

* Migrate dependent source repository and move to *beta* phase
* [feature] new module, "``clitool.textio``" to map text inputs
* [feature] ``CliHandler`` accepts "delimiter" keyword
* [feature] ``clitool.accesslog.parse`` is introduced to change parsed keys
* [deprecate] ``clitool.accesslog.logentry`` is deprecated
* [deprecate] ``clitool.processor.CsvHandler`` is deprecated
* [deprecate] ``clitool.processor.RowMapper`` is deprecated
* [backward compat break] remove deprecated features, 

  * "analyzer" keyword in ``clitool.cli.clistream``
  * ``clitool.processor.clistream``

