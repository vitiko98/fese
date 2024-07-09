from fese.container import _ffmpeg_call


def test_item():
    return
    _ffmpeg_call(
        [
            "ffmpeg",
            "-i",
            "/home/victor/Videos/Le.Samourai.mkv",
            "-map",
            "0:0",
            "test.srt",
            "-y",
        ],
        lambda d: None,
        lambda d: print(d),
    )
