#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from fese.disposition import FFprobeSubtitleDisposition


@pytest.fixture
def disposition():
    yield FFprobeSubtitleDisposition(
        {
            "default": 0,
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
        }
    )


def test_init(disposition):
    for value in disposition.__dict__.values():
        assert not value

    assert disposition.default is False
    assert disposition.suffix == ""


def test_language_kwargs(disposition):
    assert disposition.language_kwargs() == {"hi": False, "forced": False}


@pytest.mark.parametrize(
    "item,expected",
    [
        ({}, ""),
        ({"hearing_impaired": 0}, ""),
        ({"hearing_impaired": 1}, "hearing_impaired"),
        ({"forced": 1}, "forced"),
        ({"comment": 1}, "comment"),
        ({"karaoke": 1}, "karaoke"),
    ],
)
def test_suffix(item, expected):
    assert FFprobeSubtitleDisposition(item).suffix == expected


@pytest.mark.parametrize(
    "title,key",
    [
        ("CommenTaRy", "comment"),
        ("forCed", "forced"),
        ("non-english", "forced"),
        ("non english", "forced"),
        ("kaRaoke", "karaoke"),
        ("sdH", "hearing_impaired"),
        ("cc", "hearing_impaired"),
        ("siGns", "visual_impaired"),
    ],
)
def test_update_from_tags(title, key):
    disposition = FFprobeSubtitleDisposition({})
    disposition.update_from_tags({"title": title})
    assert getattr(disposition, key) is True
    assert disposition.generic is False
    assert disposition.suffix == key
