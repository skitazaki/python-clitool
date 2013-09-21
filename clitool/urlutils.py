#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" urllib wrapper.

This module is executable to download somethings.

    $ URL=http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip
    $ python -m clitool.urlutils $URL
"""

import logging
import os
import urllib

from six import PY3
if PY3:
    import urllib.parse
    urlparse = urllib.parse.urlparse
    parse_qs = urllib.parse.parse_qs
else:
    import urlparse as urlparse2
    urlparse = urlparse2.urlparse
    parse_qs = urlparse2.parse_qs


def download(url):
    o = urlparse(url)
    if not (o[0] and o[1]):
        msg = "'%s' is not valid URL."
        tup = (url,)
        raise ValueError(msg % tup)
    if not '.' in o[1]:
        msg = "'%s' does not have server name."
        tup = (url,)
        raise ValueError(msg % tup)
    # Check the document for return value attributes.
    # http://docs.python.org/library/urlparse.html#urlparse.urlparse
    # "index 2" means "path" attribute, Hierarchical path.
    path = o[2]
    fname = os.path.basename(path)
    if not fname:
        logging.debug("No file name is defined by URL, use host name.")
        fname = o[1].replace('.', '_')
    if os.path.exists(fname):
        logging.warn("%s already exists, overwrite it.", fname)
    logging.info("Download: %s -> %s", url, fname)
    try:
        urllib.urlretrieve(url, fname)
        return fname
    except IOError:
        import sys
        e = sys.exc_info()[1]
        logging.error(e)


if __name__ == '__main__':
    from clitool.cli import parse_arguments

    args = parse_arguments(urls=dict(nargs="+", metavar="URL"))
    results = [download(url) for url in args.urls]
    args.output.write("\n".join(filter(lambda s: s, results)))
    args.output.write("\n")

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
