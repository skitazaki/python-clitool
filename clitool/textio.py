#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Text I/O utilities.

Type mapping follows the rule of "`Cerberus
<http://cerberus.readthedocs.org/en/latest/>`_".

Example usage::

    import logging
    import sys

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

    s = Sequential()
    s.callback(RowMapper(FIELDS))
    s.errback(logging.error)
    for row in sys.stdin:
        dt = s(row)
        print(dt)

"""

import sys
from datetime import datetime

from six import PY3
if PY3:
    str_type = str
else:
    from clitool import DEFAULT_ENCODING
    str_type = lambda v: unicode(v, DEFAULT_ENCODING)


class Sequential(object):
    """Apply callback functions sequentially.

    If error occurs in callback, apply errback functions against catched
    exception.

    :rtype: callable
    """

    callbacks = []
    errbacks = []

    def callback(self, callback):
        self.callbacks.append(callback)

    def errback(self, errback):
        self.errbacks.append(errback)

    def __call__(self, value):
        try:
            for callback in self.callbacks:
                value = callback(value)
                if value is None:
                    return
        except Exception:
            e = sys.exc_info()[1]
            for errback in self.errbacks:
                errback(e)
            return
        return value


class RowMapper(object):

    """ Map `list_or_tuple` to dict object using given fields definition.
    If length of given data is not different from keys length,
    raise ``ValueError``.
    To accept loose inputs, change ``strict`` flag ``False``.

    If input fields are all string type, use `namedtuple
    <http://docs.python.org/2/library/collections.html>`_ in standard library
    instead. The case, however, that keys contains non-ascii characters,
    such as Japanese text, this class may be useful.

    :param fields: list of fields values.
    :type fields: tuple
    :param strict: strict match flag.
    :type strict: boolean
    :rtype: callable
    """

    def __init__(self, fields, strict=True, *args, **kwargs):
        self.fields = fields
        self.strict = strict

    def __call__(self, row, *args, **kwargs):
        """
        :param row: tuple value such as each row of csv file.
        :type row: tuple or list
        :rtype: dictionary after binding with fields values.
        """
        if not row:
            return
        if len(self.fields) != len(row) and self.strict:
            raise ValueError('Size differ: expected={}, actual={}'.format(
                len(self.fields), len(row)))
        dt = {}
        for h, v in zip(self.fields, row):
            if not v:
                continue
            k, t = h['id'], h['type']
            if t == 'string':
                dt[k] = str_type(v)
            elif t == 'integer':
                dt[k] = int(v)
            elif t == 'float':
                dt[k] = float(v)
            elif t == 'boolean':
                dt[k] = bool(v)
            elif t == 'datetime':
                dt[k] = datetime.strptime(v, h['format'])
            else:
                raise ValueError('Unknown type "{}" for "{}"'.format(t, k))
        return dt


# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
