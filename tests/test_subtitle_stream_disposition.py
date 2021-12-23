#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from fese import FFprobeSubtitleDisposition


def test_init():
    disposition = FFprobeSubtitleDisposition(
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
    for value in disposition.__dict__.values():
        assert not value

    assert disposition.default is False


@pytest.mark.parametrize(
    "title,key",
    [
        ("CommenTaRy", "comment"),
        ("forCed", "forced"),
        ("kaRaoke", "karaoke"),
        ("sdH", "hearing_impaired"),
        ("siGns", "visual_impaired"),
    ],
)
def test_update_from_tags(title, key):
    disposition = FFprobeSubtitleDisposition({})
    disposition.update_from_tags({"title": title})
    assert getattr(disposition, key) is True
    assert disposition.generic is False
