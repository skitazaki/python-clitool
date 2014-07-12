#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Utilities to parse Apache access log.

To get known about access log, see Apache HTTP server official document.
[`en <http://httpd.apache.org/docs/2.4/en/logs.html>`_]
[`ja <http://httpd.apache.org/docs/2.4/ja/logs.html>`_]

This module is also executable to parse access log record.

.. code-block:: bash

    $ tail -f /var/log/httpd/access_log | python -m clitool.accesslog

Ouput labels come from <http://ltsv.org/>
"""

import datetime
import re
import warnings
from collections import namedtuple

__all__ = ['logparse']
warnings.simplefilter("always")

# since `strptime()` is too slow, parse on regex matching.
MONTH_ABBR = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

# Probably default access log format for IPv4
LOG_FORMAT = re.compile(r"""^
    (?P<host>\S+)\s(?P<ident>\S+)\s(?P<user>\S+)\s
    \[(?P<day>\d{2})/(?P<month>[A-Z][a-z]{2})/(?P<year>\d{4}):
      (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\s
      (?P<timezone>[+-]\d{4})\]\s
    "(?P<method>[A-Z]+)?\s?(?P<path>[^?^ ]+)?\??(?P<query>\S+)?\s?
     (?P<protocol>HTTP/\d\.\d)?"\s
    (?P<status>\d{3})\s(?P<size>\d+|-)\s"(?P<referer>[^"]+)"\s"(?P<ua>[^"]*)"
    (?P<trailing>.*)
$""", re.VERBOSE)

Access = namedtuple('Access',
    '''host ident user day month year hour minute second timezone
    method path query protocol status size referer ua trailing''')


def parse(line):
    """ Parse accesslog line to map Python dictionary.

    Returned dictionary has following keys:

    - time: access time (datetime; naive)
    - utcoffset: UTC offset of access time (timedelta)
    - host: remote IP address.
    - path: HTTP request path, this will be splitted from query.
    - query: HTTP requert query string removed from "?".
    - method: HTTP request method.
    - protocol: HTTP request version.
    - status: HTTP response status code. (int)
    - size: HTTP response size, if available. (int)
    - referer: Referer header. if "-" is given, that will be ignored.
    - ua: User agent. if "-" is given, that will be ignored.
    - ident: remote logname
    - user: remote user
    - trailing: Additional information if using custom log format.

    You can use "utcoffset" with `dateutil.tz.tzoffset` like followings:

    >>> from dateutil.tz import tzoffset
    >>> e = parse(line)
    >>> tz = tzoffset(None, e['utcoffset'].total_seconds())
    >>> t = e['time'].replace(tzinfo=tz)

    :param line: one line of access log combined format
    :type line: string
    :rtype: dict
    """
    m = LOG_FORMAT.match(line)
    if m is None:
        return
    access = Access._make(m.groups())
    entry = {
        'host': access.host,
        'path': access.path,
        'query': access.query,
        'method': access.method,
        'protocol': access.protocol,
        'status': int(access.status)
    }
    entry['time'] = datetime.datetime(
        int(access.year), MONTH_ABBR[access.month], int(access.day),
        int(access.hour), int(access.minute), int(access.second))
    # Parse timezone string; "+YYMM" format.
    entry['utcoffset'] = (1 if access.timezone[0] == '+' else -1) * \
        datetime.timedelta(hours=int(access.timezone[1:3]),
                           minutes=int(access.timezone[3:5]))
    if access.ident != '-':
        entry['ident'] = access.ident
    if access.user != '-':
        entry['user'] = access.user
    if access.size != '-':
        entry['size'] = int(access.size)
    if access.referer != '-':
        entry['referer'] = access.referer
    if access.ua != '-':
        entry['ua'] = access.ua
    if access.trailing:
        entry['trailing'] = access.trailing.strip()
    return entry


def logentry(raw):
    """[DEPRECATED] Process accesslog record to map Python dictionary.

    Returned dictionary has following keys:

    - remote_address: remote IP address.
    - access_time: datetime object.
    - request_path: HTTP request path, this will be splitted from query.
    - request_query: HTTP requert query string removed from "?".
    - request_method: HTTP request method.
    - request_version: HTTP request version.
    - response_status: HTTP response status code. (int)
    - response_size: HTTP response size, if available. (int)
    - referer: Referer header. if "-" is given, that will be ignored.
    - user_agent: User agent. if "-" is given, that will be ignored.
    - ident: remote logname
    - user: remote user
    - trailing: Additional information if using custom log format.

    :param raw: one line of access log combined format
    :type raw: string
    :rtype: dict
    """
    warnings.warn('use "parse()" instead', DeprecationWarning)
    e = parse(raw.rstrip())
    if e is None:
        return
    # backward compat mapping
    entry = {
        'access_time': e['time'],
        'remote_address': e['host'],
        'request_path': e['path'],
        'request_query': e['query'],
        'request_method': e['method'],
        'request_version': e['protocol'],
        'response_status': e['status']
    }
    if 'size' in e:
        entry['response_size'] = e['size']
    if 'user_agent' in e:
        entry['user_agent'] = e['ua']
    return entry


def logparse(*args, **kwargs):
    """ Parse access log on the terminal application.
    If list of files are given, parse each file. Otherwise, parse standard
    input.

    :param args: supporting functions after processed raw log line
    :type: list of callables
    :rtype: tuple of (statistics, key/value report)
    """
    from clitool.cli import clistream
    from clitool.processor import SimpleDictReporter

    lst = [parse] + args
    reporter = SimpleDictReporter()
    stats = clistream(reporter, *lst, **kwargs)
    return stats, reporter.report()


if __name__ == '__main__':
    from six import print_
    from clitool.cli import parse_arguments, clistream

    RED = '\033[91m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    args = parse_arguments(files=dict(nargs='*'),
                color=dict(flags="--color", action="store_true"),
                status=dict(flags="--status"))

    lst = map(int, args.status.split(',')) if args.status else None

    def p(e):
        if lst and not e['status'] in lst:
            return
        colored = False
        if args.color:
            if e['status'] >= 500:
                print_(RED, end='')
                colored = True
            if e['status'] >= 400:
                print_(PURPLE, end='')
                colored = True
        for k in sorted(e.keys()):
            if e[k]:
                print_("%-16s: %s" % (k, e[k]))
        if colored:
            print_(END, end='')
        print_("-" * 40)

    stats = clistream(p, parse, files=args.files)
    print_(stats)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
