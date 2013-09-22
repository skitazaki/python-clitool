=========
Examples
=========

Example to Convert CSV into JSON
===================================

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


Example to Save Records in Database
===========================================

This script uses following modules.

* ``clitool.cli.climain`` to parse command line options.
* ``clitool.cli.cliconfig`` to load configuration along with environmental variable.

Save following configuration as ``config.ini``. ::

    [development]
    database.url=sqlite:///sample.sqlite
    database.auto=1

    [staging]
    database.url=postgresql+pypostgresql://user:pass@host/database

    [production]
    database.url=mysql://user:pass@host/database

If you set "staging" on `PYTHON_CLITOOL_ENV` environmental variable,
``cliconfig`` loads "staging" section of configuration.
Default loading section is "development".

Since next script requires "`SQLAlchemy <http://www.sqlalchemy.org/>`_",
you install it a priori. ::

    $ pip install SQLAlchemy

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    """Example to Save Records in Database.
    """

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String

    from clitool.cli import climain, cliconfig


    Session = sessionmaker()
    Base = declarative_base()


    class Address(Base):

        __tablename__ = 'address_jp'
        __table_args__ = {'sqlite_autoincrement': True}

        id = Column(Integer, primary_key=True)
        jis_code = Column(String)
        zipcode = Column(String)
        prefecture_en = Column(String)
        city_en = Column(String)
        town_en = Column(String)
        multi_zipcode = Column(Integer)
        koaza_split = Column(Integer)
        choume_view = Column(Integer)
        multi_chouiki = Column(Integer)
        update_view = Column(Integer)
        update_reason = Column(Integer)

        def __repr__(self):
            return "<Address('%s')>" % (self.jis_code)


    class SessionFactory(object):

        def __init__(self, dsl, auto=False):
            engine = create_engine(dsl)
            if auto:
                Base.metadata.create_all(engine)
            Session.configure(bind=engine)

        def create(self):
            return Session()


    @climain
    def main(config):
        cfg = cliconfig(config)
        session = SessionFactory(cfg['database.url'], cfg.get('database.auto')).create()

        for r in RECORDS:
            e = Address(**r)
            session.add(e)

        session.commit()


    # SAMPLE DATA
    RECORDS = (
        {
            "jis_code": "01101",
            "zipcode": "0600000",
            "city_en": "CHUO-KU SAPPORO-SHI",
            "prefecture_en": "HOKKAIDO",
            "multi_zipcode": False,
            "koaza_split": False,
            "choume_view": False,
            "multi_chouiki": False,
            "update_view": 0,
            "update_reason": 0
        },
        {
            "jis_code": "01101",
            "zipcode": "0640941",
            "town_en": "ASAHIGAOKA",
            "city_en": "CHUO-KU SAPPORO-SHI",
            "prefecture_en": "HOKKAIDO",
            "multi_zipcode": False,
            "koaza_split": False,
            "choume_view": True,
            "multi_chouiki": False,
            "update_view": 0,
            "update_reason": 0
        }
    )

    if __name__ == '__main__':
        main()
