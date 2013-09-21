#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import util

from clitool.processor import Streamer
from clitool import (
    PROCESSING_SUCCESS,
    PROCESSING_SKIPPED,
    PROCESSING_ERROR,
    PROCESSING_TOTAL
)


def test_streamer_linecount():
    util.log_to_stderr(util.SUBDEBUG)
    s = Streamer(processes=2)
    stats = s.consume(range(10))
    assert len(stats) == 5
    # 0 is skipped.
    assert stats[PROCESSING_TOTAL] == 10
    assert stats[PROCESSING_SUCCESS] == 9
    assert stats[PROCESSING_SKIPPED] == 1
    assert stats[PROCESSING_ERROR] == 0


# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
