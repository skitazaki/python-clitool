#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
