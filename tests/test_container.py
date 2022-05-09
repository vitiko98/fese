#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pytest

from fese.container import FFprobeVideoContainer
from fese.exceptions import ExtractionError
from fese.exceptions import InvalidSource
from fese.exceptions import UnsupportedCodec

_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture
def video():
    return FFprobeVideoContainer(os.path.join(_DATA, "file_1.mkv"))


@pytest.fixture
def mp4_video():
    return FFprobeVideoContainer(os.path.join(_DATA, "file.mp4"))


def test_init(video):
    assert video.path.endswith("file_1.mkv")


def test_get_subtitles(video):
    subtitles = video.get_subtitles()
    assert isinstance(subtitles, list)


def test_extract_subtitles_copy(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(subtitles, custom_dir=tmp_path)
    for path in subs.values():
        assert os.path.isfile(path) is True


@pytest.mark.parametrize("convert_format", ["srt", "ass", "webvtt"])
def test_extract_subtitles_convert_w_format(tmp_path, video, convert_format):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(
        subtitles, custom_dir=tmp_path, convert_format=convert_format
    )
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


def test_get_subtitles_mp4(mp4_video):
    subtitles = mp4_video.get_subtitles()
    assert isinstance(subtitles, list)


@pytest.mark.parametrize("convert_format", ["srt", "ass", "webvtt"])
def test_extract_subtitles_mp4(tmp_path, mp4_video, convert_format):
    subtitles = mp4_video.get_subtitles()
    subs = mp4_video.extract_subtitles(
        subtitles, custom_dir=tmp_path, convert_format=convert_format
    )
    for path in subs.values():
        assert os.path.isfile(path) is True


def test_subtitles_copy_mp4(tmp_path, mp4_video):
    subtitles = mp4_video.get_subtitles()
    with pytest.raises(UnsupportedCodec):
        mp4_video.extract_subtitles(subtitles, custom_dir=tmp_path)
