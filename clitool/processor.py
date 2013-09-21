#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Stream processing utility.
"""

import gzip
import json
import logging
import multiprocessing
import os
import sys
import time
import warnings
from collections import Counter

from six import PY3
from six.moves import map as imap
from six.moves import filter as ifilter

from clitool import (
    PROCESSING_REPORTING_INTERVAL,
    PROCESSING_SUCCESS,
    PROCESSING_SKIPPED,
    PROCESSING_ERROR,
    PROCESSING_TOTAL,
    PROCESSING_TIME
)

if PY3:
    import csv
    import io

    def csvreader3(fp, encoding, **kwargs):
        return csv.reader(io.TextIOWrapper(fp.buffer, encoding), **kwargs)

    csvreader = csvreader3

else:
    from ._unicodecsv import UnicodeReader

    def csvreader2(fp, encoding, **kwargs):
        return UnicodeReader(fp, encoding=encoding, **kwargs)

    csvreader = csvreader2

warnings.simplefilter("always")


class SimpleDictReporter(object):
    """ Reporting class for streamer API.
    Passing processed data as mapping object, report the key/value pair
    if value is string. To call ``report()``, you can get the result as dict.
    """

    def __init__(self, *args, **kwargs):
        self.counter = Counter()

    def __call__(self, entry):
        """
        :param entry: dictionary
        :rtype: None
        """
        if type(entry) is not dict:
            return
        for k in entry:
            v = entry[k]
            if type(v) == str:
                self.counter[k + ":" + v] += 1

    def report(self):
        """
        :rtype: dict
        """
        return dict(self.counter)


class RowMapper(object):
    """ Map `list_or_tuple` to dict object using given keys.
    If keys are not given, first `list_or_tuple` is used as keys.
    If length of given data is not different from keys length,
    no valid data is returned.

    Since this object is aimed to use with :class:`Streamer`,
    mapping is fired to call this.

    If you know header names a priori, use standard `namedtuple
    <http://docs.python.org/2/library/collections.html>`_ instead.
    But the case that keys contains non-ascii, such as Japanese text, this
    class may be useful.

    :param header: list of header values.
    :type header: tuple
    :param loose: loosly match flag.
    :type loose: bool
    """

    ERRMSG = "Couldn't map given row: header-length=%d, row-length=%d"
    LOOSEMSG = "Length is not matched: header-length=%d, row-length=%d"

    def __init__(self, header=None, loose=False, *args, **kwargs):
        self.header = header
        self.loose = loose

    def __call__(self, row, *args, **kwargs):
        """
        :param row: tuple value such as each row of csv file.
        :type row: tuple or list
        :rtype: dictionary after binding with header values.
        """
        if not row:
            return
        if self.header is None or self.header == row:
            self.header = row
            logging.info("New header is set, because no header was given.")
            return
        if len(self.header) == len(row):
            return dict(zip(self.header, row))
        if self.loose:
            logging.info(RowMapper.LOOSEMSG, len(self.header), len(row))
            return dict(zip(self.header, row))
        logging.error(RowMapper.ERRMSG, len(self.header), len(row))


# Can not recycle pool . . .
# http://stackoverflow.com/questions/5481104/multiprocessing-pool-imap-broken
class Streamer(object):

    """ Simple streaming module to accept step-by-step procedures.
    General steps are:

    1. check input value meets your requirements.
    2. parse something for your business.
    3. collect parsed value.

    Step 1 and Step 2 have to follow these rules:

    - return True to skip parsing
    - return False to report error
    - return something valid to continue processing the item

    Step 3 is arbitrary function to accept one argument such as
    :func:`list.append()`.

    :param callback: function to collect parsed value
    :type callback: callable
    :param args: callables
    :type args: list
    """

    def __init__(self, callback=None, *args, **kwargs):
        procs = tuple(filter(lambda r: r, args))
        logging.debug("%d procedures are set.", len(procs))
        self.procedures = procs
        self.collect = callback or (lambda r: r)
        self.processes = kwargs.get('processes')
        if self.processes and self.processes > multiprocessing.cpu_count():
                logging.warn("given processes is %d, count of CPU is %d" % (
                    self.processes, multiprocessing.cpu_count()))
        self.reporting_interval = PROCESSING_REPORTING_INTERVAL

    def consume(self, stream, chunksize=1):
        """ Consuming given strem object and returns processing stats.

        :param stream: streaming object to consume
        :type stream: iterable
        :rtype: dict
        """
        stats = {
            PROCESSING_TOTAL: 0,
            PROCESSING_SKIPPED: 0,
            PROCESSING_SUCCESS: 0,
            PROCESSING_ERROR: 0
        }

        def skip_unless(r):
            if r:
                return r
            stats[PROCESSING_SKIPPED] += 1
            stats[PROCESSING_TOTAL] += 1

        rs = ifilter(skip_unless, stream)
        if self.processes:
            pool = multiprocessing.Pool(processes=self.processes)
            for f in self.procedures:
                rs = pool.imap_unordered(f, ifilter(skip_unless, rs),
                        chunksize=chunksize)
        else:
            for f in self.procedures:
                rs = imap(f, ifilter(skip_unless, rs))
        start = time.time()
        i = 0
        try:
            while 1:
                processed = next(rs)
                if processed is None:
                    stats[PROCESSING_SKIPPED] += 1
                elif processed is False:
                    stats[PROCESSING_ERROR] += 1
                else:
                    stats[PROCESSING_SUCCESS] += 1
                    self.collect(processed)
                i += 1
                stats[PROCESSING_TOTAL] += 1
                if i % self.reporting_interval == 0:
                    logging.info(" ===> Processed %dth item <=== ", i)
        except StopIteration:
            pass
        except KeyboardInterrupt:
            logging.info("Stopped by user interruption at %dth item.", i)
            raise
        except:
            e = sys.exc_info()[1]
            logging.error(e)
            raise
        finally:
            if self.processes:
                pool.close()
                pool.join()
            stats[PROCESSING_TIME] = time.time() - start
            logging.info(
                "STATS: total=%d, skipped=%d, success=%d, error=%d on %f[sec]",
                stats[PROCESSING_TOTAL], stats[PROCESSING_SKIPPED],
                stats[PROCESSING_SUCCESS], stats[PROCESSING_ERROR],
                stats[PROCESSING_TIME])
            return stats


class CliHandler(object):

    """ Simple command line arguments handler.

    :param streamer: streaming object
    :type streamer: Streamer
    """

    def __init__(self, streamer):
        self.streamer = streamer

    def reader(self, fp, encoding=None):
        """ Simple `open` wrapper for several file types.
        This supports ``.gz`` and ``.json``.

        :param fp: opened file
        :type fp: file pointer
        :param encoding: encoding of opened file
        :type encoding: string
        :rtype: file pointer
        """
        _, suffix = os.path.splitext(fp.name)
        if suffix == '.gz':
            fp.close()
            return gzip.open(fp.name)
        elif suffix == '.json':
            return json.load(fp)
        return fp

    def handle(self, files, encoding, chunksize=1):
        """ Handle given files with given encoding.

        :param files: opened files.
        :type files: list
        :param encoding: encoding of opened file
        :type encoding: string
        :param chunksize: a number of chunk
        :type chunksize: int
        :rtype: list
        """
        stats = []
        if files:
            logging.info("Input file count: %d", len(files))
            for fp in files:
                fname = fp.name
                logging.info("Start processing: %s", fname)
                reader = self.reader(fp, encoding)
                parsed = self.streamer.consume(reader, chunksize)
                logging.info("End processing: %s", fname)
                parsed['file'] = fname
                stats.append(parsed)
                if not fp.closed:
                    fp.close()
        else:
            reader = self.reader(sys.stdin, encoding)
            parsed = self.streamer.consume(reader)
            stats.append(parsed)
        return stats


class CsvHandler(CliHandler):

    def reader(self, fp, encoding):
        return csvreader(fp, encoding)


def clistream(reporter, *args, **kwargs):
    warnings.warn("use 'clitool.cli.clistream' instead.", DeprecationWarning)
    from .cli import clistream as new_clistream
    return new_clistream(reporter, *args, **kwargs)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
