#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clitool.config import ConfigLoader

import os
import sys

if sys.version_info[0] == 3:
    from io import StringIO
else:
    from cStringIO import StringIO

from clitool import RUNNING_MODE_ENVKEY

BASEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

JSON = '''
{
    "development": {
        "database": {
            "url": "sqlite:///:memory:",
            "auto": true
        }
    },
    "test": {
        "database": {
            "url": "sqlite:///test.sqlite",
            "auto": true
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
'''

INI = '''
[development]
database.url=sqlite:///:memory:

[staging]
database.url=postgresql+pypostgresql://user:pass@host/database

[production]
database.url=mysql://user:pass@host/database
'''

YAML = '''
development:
  database:
    url: "sqlite:///:memory:"

staging:
  database:
    url: "postgresql+pypostgresql://user:pass@host/database"

production:
  database:
    url: "mysql://user:pass@host/database"
'''


def test_json():
    fp = StringIO(JSON)
    loader = ConfigLoader(fp, 'json')
    config = loader.load()
    assert config
    assert 'url' in config['database']
    assert config['database']['url'] == 'sqlite:///:memory:'


def test_json2():
    os.environ[RUNNING_MODE_ENVKEY] = 'staging'
    fp = StringIO(JSON)
    loader = ConfigLoader(fp, 'json')
    config = loader.load()
    assert config
    assert 'url' in config['database']
    assert config['database']['url'] == \
        'postgresql+pypostgresql://user:pass@host/database'
    del os.environ[RUNNING_MODE_ENVKEY]


def test_json3():
    os.environ[RUNNING_MODE_ENVKEY] = 'production'
    fp = StringIO(JSON)
    loader = ConfigLoader(fp, 'json')
    config = loader.load()
    assert config
    assert 'url' in config['database']
    assert config['database']['url'] == \
        'mysql+mysqlconnector://user:pass@host/database'
    del os.environ[RUNNING_MODE_ENVKEY]


def test_ini():
    fp = StringIO(INI)
    loader = ConfigLoader(fp, 'ini')
    config = loader.load()
    assert config
    assert 'database.url' in config
    assert config['database.url'] == 'sqlite:///:memory:'


def test_ini_flip():
    fp = StringIO(INI)
    loader = ConfigLoader(fp, 'ini')
    config = loader.flip()
    assert config
    db = config['database.url']
    assert db['development'] == 'sqlite:///:memory:'
    assert db['production'] == 'mysql://user:pass@host/database'
    assert db['staging'] == 'postgresql+pypostgresql://user:pass@host/database'


def test_json_flip():
    fp = StringIO(JSON)
    loader = ConfigLoader(fp, 'json')
    config = loader.flip()
    assert config
    db = config['database']
    assert db['development']['url'] == 'sqlite:///:memory:'
    assert db['production']['url'] == \
        'mysql+mysqlconnector://user:pass@host/database'
    assert db['staging']['url'] == \
        'postgresql+pypostgresql://user:pass@host/database'


def test_yaml_flip():
    try:
        import pyyaml
        print(pyyaml)  # avoid pyflakes error
    except:
        # pass
        return
    fp = StringIO(JSON)
    loader = ConfigLoader(fp, 'yaml')
    config = loader.flip()
    assert config
    db = config['database']
    assert db['development']['url'] == 'sqlite:///:memory:'
    assert db['production']['url'] == \
        'mysql://user:pass@host/database'
    assert db['staging']['url'] == \
        'postgresql+pypostgresql://user:pass@host/database'

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
