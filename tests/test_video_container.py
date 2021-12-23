#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pytest

from fese import ExtractionError
from fese import FFprobeVideoContainer
from fese import InvalidSource

_VIDEO = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "file_1.mkv")


@pytest.fixture
def video():
    return FFprobeVideoContainer(_VIDEO)


def test_init(video):
    assert video.path == _VIDEO


def test_get_subtitles(video):
    subtitles = video.get_subtitles()
    assert isinstance(subtitles, list)


def test_extract_subtitles(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(subtitles, custom_dir=tmp_path)
    for path in subs.values():
        assert os.path.isfile(path) is True


def test_get_subtitles_timeout(video):
    with pytest.raises(InvalidSource):
        assert video.get_subtitles(timeout=0.0001)


def test_extract_subtitles_timeout(video):
    with pytest.raises(ExtractionError):
        subtitles = video.get_subtitles()
        if not subtitles:
            pytest.skip()

        assert video.extract_subtitles(subtitles, timeout=0.0001)
