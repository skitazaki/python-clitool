#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Utilities to parse Apache access log.

To get known about access log, see Apache HTTP server official document.
[`en <http://httpd.apache.org/docs/2.4/en/logs.html>`_]
[`ja <http://httpd.apache.org/docs/2.4/ja/logs.html>`_]

This module is also executable to parse access log record.

.. code-block:: bash

    $ tail -f /var/log/httpd/access_log | python -m clitool.accesslog

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


def logentry(raw):
    """ Process accesslog record to map Python dictionary.

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

    :param access: internal object which represent accesslog record
    :type access: Access
    :rtype: dict
    """
    m = LOG_FORMAT.match(raw.rstrip())
    if m is None:
        return
    access = Access._make(m.groups())
    entry = {
        'remote_address': access.host,
        'request_path': access.path,
        'request_query': access.query,
        'request_method': access.method,
        'request_version': access.protocol,
        'response_status': int(access.status)
    }
    entry['access_time'] = datetime.datetime(
        int(access.year), MONTH_ABBR[access.month], int(access.day),
        int(access.hour), int(access.minute), int(access.second))
    if access.ident != '-':
        entry['ident'] = access.ident
    if access.user != '-':
        entry['user'] = access.user
    if access.size != '-':
        entry['response_size'] = int(access.size)
    if access.referer != '-':
        entry['referer'] = access.referer
    if access.ua != '-':
        entry['user_agent'] = access.ua
    if access.trailing:
        entry['trailing'] = access.trailing.strip()
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

    lst = [logentry]
    analyzer = kwargs.get('analyzer')
    if analyzer:
        warnings.warn("analyzer keyword is deprecated.", DeprecationWarning)
        lst.append(analyzer)
    lst += args
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
        if lst and not e['response_status'] in lst:
            return
        colored = False
        if args.color:
            if e['response_status'] >= 500:
                print_(RED, end='')
                colored = True
            if e['response_status'] >= 400:
                print_(PURPLE, end='')
                colored = True
        for k in sorted(e.keys()):
            if e[k]:
                print_("%-16s: %s" % (k, e[k]))
        if colored:
            print_(END, end='')
        print_("-" * 40)

    stats = clistream(p, logentry, files=args.files)
    print_(stats)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
