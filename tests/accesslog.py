#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from clitool.accesslog import parse


def test_accesslog_regex():
    TESTS = '''
127.0.0.1 - - [22/Aug/2011:10:02:03 +0900] "GET / HTTP/1.1" 200 151 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0) Gecko/20100101 Firefox/6.0"
127.0.0.1 - - [22/Aug/2011:10:02:03 +0900] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0) Gecko/20100101 Firefox/6.0"
127.0.0.1 - - [14/Feb/2012:09:45:28 +0900] "GET /favicon.ico HTTP/1.1" 404 168 "-" ""
127.0.0.1 - - [14/Feb/2012:11:39:50 +0900] "-" 400 0 "-" "-"
127.0.0.1 - firstuser [11/Apr/2012:11:04:52 +0900] "GET /simple/ HTTP/1.1" 200 46 "-" "Python-urllib/2.7"
'''.strip().split('\n')
    error = []
    for t in TESTS:
        e = parse(t)
        if e is None:
            error.append(t)
    if error:
        print('Failed inputs:\n')
        print('\t', '\n\t'.join(error))
        assert False, "see above outputs"


# See official document about "tzinfo" class.
ZERO = datetime.timedelta(0)


class UTC(datetime.tzinfo):

    def utcoffset(self, dt):
        return ZERO

    def dst(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"


class JST(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=9)

    def dst(self, dt):
        return ZERO

    def tzname(self, dt):
        return "JST"


def test_accesslog_timezone():
    t = '''
127.0.0.1 - - [22/Aug/2011:10:02:03 +0900] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0) Gecko/20100101 Firefox/6.0"
127.0.0.1 - - [22/Aug/2011:10:02:03 -0900] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0) Gecko/20100101 Firefox/6.0"
'''.strip().split('\n')
    # Parse and test first line.
    e = parse(t[0])
    assert e['time'] == datetime.datetime(2011, 8, 22, 10, 2, 3)
    assert e['utcoffset'] == datetime.timedelta(hours=9)
    assert e['utcoffset'].total_seconds() == 9 * 3600
    jst = JST()
    utc = UTC()
    # make datetime object "naive" to "aware".
    d = e['time'].replace(tzinfo=jst)
    assert d.day == 22
    assert d.hour == 10
    u = d.astimezone(utc)
    assert u.day == 22
    assert u.hour == 1  # 1 hour = 10 - 9
    # Parse and test second line.
    e = parse(t[1])
    assert e['time'] == datetime.datetime(2011, 8, 22, 10, 2, 3)
    assert e['utcoffset'] == datetime.timedelta(hours=-9)
    assert e['utcoffset'].total_seconds() == -9 * 3600

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
