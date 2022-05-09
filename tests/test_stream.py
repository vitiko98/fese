#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

import pytest

from fese.exceptions import LanguageNotFound
from fese.exceptions import UnsupportedCodec
from fese.stream import FFprobeSubtitleStream


@pytest.fixture
def sub_stream():
    return {
        "index": 3,
        "codec_name": "ass",
        "codec_long_name": "ASS (Advanced SSA) subtitle",
        "codec_type": "subtitle",
        "codec_tag_string": "[0][0][0][0]",
        "codec_tag": "0x0000",
        "r_frame_rate": "0/0",
        "avg_frame_rate": "0/0",
        "time_base": "1/1000",
        "start_pts": 0,
        "start_time": "0.000000",
        "duration_ts": 1218718,
        "duration": "1218.718000",
        "disposition": {
            "default": 1,
            "dub": 0,
            "original": 0,
            "comment": 0,
            "lyrics": 0,
            "karaoke": 0,
            "forced": 0,
            "hearing_impaired": 0,
            "visual_impaired": 0,
            "clean_effects": 0,
            "attached_pic": 0,
            "timed_thumbnails": 0,
        },
        "tags": {"language": "eng", "title": "English"},
    }


@pytest.fixture
def subtitle(sub_stream):
    return FFprobeSubtitleStream(sub_stream)


def test_init(subtitle):
    assert subtitle.extension == "ass"
    assert subtitle.duration == timedelta(seconds=1218.71800)
    assert subtitle.tags is not None
    assert subtitle.disposition is not None


def test_extension(subtitle):
    assert subtitle.extension == "ass"


def test_language(subtitle):
    assert subtitle.language.alpha3 == "eng"


def test_suffix(subtitle):
    assert subtitle.suffix == "en.ass"


def test_disposition(subtitle):
    assert subtitle.disposition.hearing_impaired == False


def test_durations(subtitle):
    assert subtitle.duration_ts == timedelta(milliseconds=1218718)
    assert subtitle.duration == timedelta(seconds=1218.718)


def test_copy_args(subtitle):
    assert subtitle.copy_args("test") == [
        "-map",
        "0:3",
        "-c:s",
        "copy",
        "-f",
        "ass",
        "test",
    ]


def test_convert_ars(subtitle):
    assert subtitle.convert_args("srt", "test") == [
        "-map",
        "0:3",
        "-f",
        "srt",
        "test",
    ]


def test_unsupported_codec():
    with pytest.raises(UnsupportedCodec):
        return FFprobeSubtitleStream({"codec_name": "avc", "index": 1})


def test_language_not_found():
    with pytest.raises(LanguageNotFound):
        return FFprobeSubtitleStream(
            {"codec_name": "ass", "index": 1, "tags": {"language": "und"}}
        )


def test_convert_unsupported_codec():
    stream = FFprobeSubtitleStream(
        {"codec_name": "hdmv_pgs_subtitle", "index": 1, "tags": {"language": "eng"}}
    )
    with pytest.raises(UnsupportedCodec):
        stream.convert_args("srt", "test")


def test_convert_unsupported_codec_2():
    stream = FFprobeSubtitleStream(
        {"codec_name": "subrip", "index": 1, "tags": {"language": "eng"}}
    )
    with pytest.raises(UnsupportedCodec):
        stream.convert_args("unknown", "test")
