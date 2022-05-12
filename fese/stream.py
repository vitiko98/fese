# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import timedelta
import logging

from .disposition import FFprobeSubtitleDisposition
from .exceptions import UnsupportedCodec
from .tags import FFprobeGenericSubtitleTags

logger = logging.getLogger(__name__)


class FFprobeSubtitleStream:
    """Base class for FFprobe (FFmpeg) extractable subtitle streams."""

    def __init__(self, stream: dict):
        """
        :raises: LanguageNotFound, UnsupportedCodec
        """
        self.index = int(stream["index"])
        self.codec_name = stream["codec_name"]

        try:
            self._codec = _codecs[self.codec_name]
        except KeyError:
            raise UnsupportedCodec(f"{self.codec_name} is not supported")

        self.r_frame_rate = stream.get("r_frame_rate")
        self.avg_frame_rate = stream.get("avg_frame_rate")
        self.start_time = timedelta(seconds=float(stream.get("start_time", 0)))
        self.start_pts = timedelta(milliseconds=int(stream.get("start_pts", 0)))
        self.duration_ts = timedelta(milliseconds=int(stream.get("duration_ts", 0)))
        self.duration = timedelta(seconds=float(stream.get("duration", 0)))

        self.tags = FFprobeGenericSubtitleTags.detect_cls_from_data(
            stream.get("tags", {})
        )
        self.disposition = FFprobeSubtitleDisposition(stream.get("disposition", {}))

        if stream.get("tags") is not None:
            self.disposition.update_from_tags(stream["tags"])

    def convert_args(self, codec_name, outfile):
        if not any(codec_name == item["copy_format"] for item in _codecs.values()):
            raise UnsupportedCodec(f"Unknown codec: {codec_name}")

        if not self._codec["convert"]:
            raise UnsupportedCodec(
                f"{self.codec_name} codec doesn't support conversion"
            )

        return ["-map", f"0:{self.index}", "-f", codec_name, outfile]

    def copy_args(self, outfile):
        if not self._codec["copy"] or not self._codec["copy_format"]:
            raise UnsupportedCodec(f"{self.codec_name} doesn't support copy")

        return [
            "-map",
            f"0:{self.index}",
            "-c:s",
            "copy",
            "-f",
            self._codec["copy_format"],
            outfile,
        ]

    @property
    def language(self):
        # Legacy
        return self.tags.language

    @property
    def extension(self):
        return self._codec["copy_format"] or ""

    @property
    def suffix(self):
        return ".".join(
            item
            for item in (
                self.tags.suffix,
                self.disposition.suffix,
            )
            if item
        )

    def __repr__(self) -> str:
        return f"<{self.codec_name.upper()}: {self.tags}@{self.disposition}>"


_codecs = {
    "ass": {"type": "text", "copy": True, "copy_format": "ass", "convert": True},
    "subrip": {"type": "text", "copy": True, "copy_format": "srt", "convert": True},
    "webvtt": {"type": "text", "copy": True, "copy_format": "webvtt", "convert": True},
    "mov_text": {"type": "text", "copy": False, "copy_format": "", "convert": True},
    "hdmv_pgs_subtitle": {
        "type": "bitmap",
        "copy": True,
        "copy_format": "sup",
        "convert": False,
    },
    "dvb_subtitle": {
        "type": "bitmap",
        "copy": True,
        "copy_format": "sup",
        "convert": False,
    },
    "dvd_subtitle": {
        "type": "bitmap",
        "copy": True,
        "copy_format": "sup",
        "convert": False,
    },
}
