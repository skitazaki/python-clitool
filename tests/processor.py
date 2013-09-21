#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] == 3:
    from io import StringIO
else:
    from cStringIO import StringIO

from clitool.processor import (
    CliHandler,
    RowMapper,
    SimpleDictReporter,
    Streamer
)

from clitool import (
    PROCESSING_SUCCESS,
    PROCESSING_SKIPPED,
    PROCESSING_ERROR,
    PROCESSING_TOTAL
)

ACCESSLOG = """
119.63.196.88 - - [17/Oct/2012:19:09:33 +0900]
178.154.243.119 - - [17/Oct/2012:19:11:49 +0900]
201.140.105.102 - - [17/Oct/2012:19:16:00 +0900]
210.237.84.86 - - [17/Oct/2012:21:03:37 +0900]
211.154.213.122 - - [17/Oct/2012:21:18:35 +0900]
211.154.213.122 - - [17/Oct/2012:21:18:35 +0900]
211.154.213.122 - - [17/Oct/2012:21:18:35 +0900]
211.154.213.122 - - [17/Oct/2012:21:18:35 +0900]
""".strip().split('\n')


def test_streamer_linecount():
    s = Streamer()
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 8
    assert stats[PROCESSING_SUCCESS] == 8
    assert stats[PROCESSING_SKIPPED] == 0
    assert stats[PROCESSING_ERROR] == 0


def test_streamer_proc_error():

    def error(*args):
        return False

    s = Streamer(None, error)
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 8
    assert stats[PROCESSING_SUCCESS] == 0
    assert stats[PROCESSING_SKIPPED] == 0
    assert stats[PROCESSING_ERROR] == 8


def test_streamer_proc_failure():

    def raise_error(*args):
        assert False

    s = Streamer(None, raise_error)
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 0
    assert stats[PROCESSING_SUCCESS] == 0
    assert stats[PROCESSING_SKIPPED] == 0
    assert stats[PROCESSING_ERROR] == 0


def test_streamer_skip():

    def noop(*args):
        pass

    s = Streamer(None, noop)
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 8
    assert stats[PROCESSING_SUCCESS] == 0
    assert stats[PROCESSING_SKIPPED] == 8
    assert stats[PROCESSING_ERROR] == 0


def test_streamer_ipaddrcount():

    def parse_log_line(raw):
        ipaddr = raw.split()[0]
        return {'ipaddr': ipaddr}

    reporter = SimpleDictReporter()
    s = Streamer(reporter, parse_log_line)
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 8
    assert stats[PROCESSING_SUCCESS] == 8
    assert stats[PROCESSING_SKIPPED] == 0
    assert stats[PROCESSING_ERROR] == 0
    results = reporter.report()
    assert len(results) == 5


def test_streamer_ipaddrcount2():

    def parse_log_line(raw):
        return raw.split()[0]

    results = []
    s = Streamer(results.append, parse_log_line)
    stats = s.consume(ACCESSLOG)
    assert len(stats) == 5
    assert stats[PROCESSING_TOTAL] == 8
    assert stats[PROCESSING_SUCCESS] == 8
    assert stats[PROCESSING_SKIPPED] == 0
    assert stats[PROCESSING_ERROR] == 0
    assert len(results) == 8


def test_simple_dict_reporter():
    reporter = SimpleDictReporter()
    reporter(None)
    reporter(True)
    reporter(False)
    reporter(1)
    reporter(-1)
    reporter(0)
    reporter("ABC")
    reporter([])
    reporter({})
    reporter(())
    report = reporter.report()
    assert len(report) == 0, "dict is not given"
    reporter({'sample_bool': True})
    reporter({'sample_int': 0})
    reporter({'sample_str': "SAMPLE"})
    reporter({'sample_list': []})
    assert len(report) == 0, "not live element"
    report = reporter.report()
    assert len(report) == 1
    assert report['sample_str:SAMPLE'] == 1
    reporter({'sample_str': "SAMPLE"})
    report = reporter.report()
    assert len(report) == 1
    assert report['sample_str:SAMPLE'] == 2, "incremented"


def test_row_mapper():
    mapper = RowMapper()
    r = mapper(['field1', 'field2', 'field3'])
    assert r is None
    r = mapper(())
    assert r is None
    r = mapper((1, 2, 3))
    assert len(r) == 3
    assert r['field1'] == 1
    assert r['field2'] == 2
    assert r['field3'] == 3
    r = mapper((1, 2, 3, 4))
    assert r is None


def test_row_mapper_missing_field():
    mapper = RowMapper(loose=True)
    r = mapper(['field1', 'field2', 'field3', 'field4'])
    assert r is None

    r = mapper(())
    assert r is None

    r = mapper((1, 2, 3))
    assert len(r) == 3
    assert r['field1'] == 1
    assert r['field2'] == 2
    assert r['field3'] == 3

    r = mapper((1, 2, 3, 4))
    assert len(r) == 4
    assert r['field1'] == 1
    assert r['field2'] == 2
    assert r['field3'] == 3
    assert r['field4'] == 4

    r = mapper((1, 2, 3, 4, 5))
    assert len(r) == 4
    assert r['field1'] == 1
    assert r['field2'] == 2
    assert r['field3'] == 3
    assert r['field4'] == 4


def test_clihander():
    dt = []
    mapper = RowMapper(['A', 'B', 'C'])
    s = Streamer(dt.append, mapper)
    handler = CliHandler(s, delimiter=',')
    sys.stdin = StringIO()
    sys.stdin.write('A,B,C\n1,2,3')
    sys.stdin.seek(0)
    handler.handle(None, 'utf-8')
    print dt
    assert len(dt) == 1
    r = dt[0]
    assert r['A'] == '1'
    assert r['B'] == '2'
    assert r['C'] == '3'

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
