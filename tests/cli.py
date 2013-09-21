#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clitool.cli import parse_arguments
from clitool import DEFAULT_ENCODING

import os
import sys


def test_default_settings():
    sys.argv = [__file__, ]
    #sys.argv = ['python', __file__]
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

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
