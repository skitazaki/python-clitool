#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from six import StringIO

from clitool.cli import parse_arguments, clistream
from clitool import DEFAULT_ENCODING


def test_default_settings():
    sys.argv = [__file__, ]
    # sys.argv = ['python', __file__]
    cwd = os.getcwd()
    args = parse_arguments()
    assert args.basedir == cwd
    assert args.config is None
    assert args.input_encoding == DEFAULT_ENCODING
    assert args.output_encoding == DEFAULT_ENCODING
    assert args.output == sys.stdout


def test_logging_settings():
    sys.argv = [__file__, '-v']
    args = parse_arguments()
    assert args.verbose == 1
    sys.argv = [__file__, '-vv']
    args = parse_arguments()
    assert args.verbose == 2
    sys.argv = [__file__, '-vvv']
    args = parse_arguments()
    assert args.verbose == 3


def test_clistream():
    dt = []
    sys.stdin = StringIO()
    sys.stdin.write('A,B,C\n1,2,3\n')
    sys.stdin.seek(0)
    clistream(dt.append, lambda l: l.rstrip('\r\n'))
    assert len(dt) == 2
    assert dt[0] == 'A,B,C'
    assert dt[1] == '1,2,3'


def test_clistream_tsv():
    dt = []
    sys.stdin = StringIO()
    sys.stdin.write('A,B,C\n1,2,3\n')
    sys.stdin.seek(0)
    clistream(dt.append, delimiter=',')
    assert len(dt) == 2
    assert dt[0] == ['A', 'B', 'C']
    assert dt[1] == ['1', '2', '3']

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
