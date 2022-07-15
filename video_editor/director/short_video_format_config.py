from dataclasses import dataclass


@dataclass
class ShortVideoFormatConfig:
    width = 1080
    height = 1920
    fps = 30
    bitrate_mb = 20
    audio_bitrate_mb = 5
    audio_sample_rate = 44100
    audio_channels = 2
    video_extension = 'mp4'
    max_video_duration_seconds = 60