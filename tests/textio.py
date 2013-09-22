# -*- coding: utf-8 -*-

from clitool.textio import Sequential, RowMapper

FIELDS = (
    {'id': 'id', 'type': 'string'},
    {'id': 'updated', 'type': 'datetime', 'format': '%Y-%m-%dT%H:%M:%SZ'},
    {'id': 'name', 'type': 'string'},
    {'id': 'latitude', 'type': 'float'},
    {'id': 'longitude', 'type': 'float'},
    {'id': 'zipcode', 'type': 'string'},
    {'id': 'kind', 'type': 'string', 'default': 'UNKNOWN'},
    {'id': 'update_type', 'type': 'integer'}
)


def test_row_mapper():
    mapper = RowMapper(FIELDS)
    r = mapper('1,2013-09-20T12:00:00Z,A,35.5,136.2,1112222,,1'.split(','))
    assert r
    assert r['id'] == '1'
    assert r['updated'].strftime('%Y-%m-%dT%H:%M:%S') == '2013-09-20T12:00:00'
    assert r['name'] == 'A'
    assert r['latitude'] == 35.5
    assert r['longitude'] == 136.2
    assert r['zipcode'] == '1112222'
    assert not 'kind' in r, r['kind']
    assert r['update_type'] == 1


def test_sequential():
    s = Sequential()
    s.callback(RowMapper(FIELDS))
    r = s('1,2013-09-20T12:00:00Z,A,35.5,136.2,1112222,,1'.split(','))
    assert r
    assert r['id'] == '1'
    assert r['updated'].strftime('%Y-%m-%dT%H:%M:%S') == '2013-09-20T12:00:00'
    assert r['name'] == 'A'
    assert r['latitude'] == 35.5
    assert r['longitude'] == 136.2
    assert r['zipcode'] == '1112222'
    assert not 'kind' in r, r['kind']
    assert r['update_type'] == 1

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
