#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pysubs2
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


@pytest.mark.parametrize("convert_format", ["srt", "ass", "webvtt"])
def test_extract_subtitles_convert_w_format(tmp_path, video, convert_format):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(
        subtitles,
        custom_dir=tmp_path,
        convert_format=convert_format,
        progress_callback=lambda d: print(f"Progress: {d}"),
    )
    for path in subs.values():
        _is_text_sub_file_valid(path)
        assert os.path.isfile(path) is True
        assert path.endswith(f".{convert_format}")
        assert _is_text_sub_file_valid(path)


def test_extract_subtitles_convert_w_o_format(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(subtitles, custom_dir=tmp_path, convert_format=None)
    for path in subs.values():
        assert os.path.isfile(path) is True
        assert path.endswith(".srt")
        assert _is_text_sub_file_valid(path)


def test_extract_subtitles_convert_w_basename_callback(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.extract_subtitles(
        subtitles,
        custom_dir=tmp_path,
        basename_callback=lambda d: "file.dummy",
        progress_callback=lambda d: print(f"Progress: {d}"),
    )
    for path in subs.values():
        assert os.path.basename(path) == "file.dummy"
        assert _is_text_sub_file_valid(path)


def test_extract_subtitles_copy(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.copy_subtitles(subtitles, custom_dir=tmp_path)
    for path in subs.values():
        assert os.path.isfile(path) is True
        assert path.endswith(".ass")
        assert _is_text_sub_file_valid(path)


def test_extract_subtitles_copy_w_basename_callback(tmp_path, video):
    subtitles = video.get_subtitles()
    subs = video.copy_subtitles(
        subtitles, custom_dir=tmp_path, basename_callback=lambda d: "file.dummy"
    )
    for path in subs.values():
        assert os.path.basename(path) == "file.dummy"
        assert _is_text_sub_file_valid(path)


def test_get_subtitles_raises_timeout(video):
    with pytest.raises(InvalidSource):
        assert video.get_subtitles(timeout=0.0001)


def test_extract_subtitles_raises_timeout(video):
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
        assert path.endswith(f".{convert_format}")
        assert _is_text_sub_file_valid(path)


def test_subtitles_copy_mp4_no_fallback_raises_unsupported_codec(tmp_path, mp4_video):
    subtitles = mp4_video.get_subtitles()
    with pytest.raises(UnsupportedCodec) as exc_info:
        mp4_video.copy_subtitles(
            subtitles, custom_dir=tmp_path, fallback_to_convert=False
        )

    assert "doesn't support copy" in str(exc_info.value)


def test_subtitles_copy_mp4_w_fallback(tmp_path, mp4_video):
    subtitles = mp4_video.get_subtitles()
    subs = mp4_video.copy_subtitles(
        subtitles, custom_dir=tmp_path, fallback_to_convert=True
    )
    for path in subs.values():
        assert os.path.isfile(path) is True
        assert path.endswith(f".srt")
        assert _is_text_sub_file_valid(path)


def _is_text_sub_file_valid(path):
    loaded = pysubs2.load(path)
    return len(loaded.events) > 0
