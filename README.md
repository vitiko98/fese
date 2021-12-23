# fese

A library to extract FFmpeg subtitle streams

## Usage

```python
import logging
import sys

import fese

logging.basicConfig(level=logging.DEBUG)

video_path = sys.argv[1]

video = fese.FFprobeVideoContainer(video_path)

subtitles = video.get_subtitles()

paths = video.extract_subtitles(subtitles)
print(paths)
```
