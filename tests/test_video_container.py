#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pytest

from fese import ExtractionError
from fese import FFprobeVideoContainer
from fese import InvalidSource

_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture
def video():
    return FFprobeVideoContainer(os.path.join(_DATA, "file_1.mkv"))


@pytest.fixture
def pgs_video():
    return FFprobeVideoContainer(os.path.join(_DATA, "file_2.mkv"))


def test_init(video):
    assert video.path.endswith("file_1.mkv")


def test_get_subtitles(video):
    subtitles = video.get_subtitles()
    assert isinstance(subtitles, list)


@pytest.mark.skipif(
    not os.path.isfile(os.path.join(_DATA, "file_2.mkv")), reason="Test file not found"
)
def test_extract_subtitles_pgs(tmp_path, pgs_video):
    subtitles = pgs_video.get_subtitles()
    subs = pgs_video.extract_subtitles(subtitles, custom_dir=tmp_path)
    for path in subs.values():
        assert os.path.isfile(path) is True


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
