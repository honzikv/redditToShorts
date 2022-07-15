from datetime import datetime

from reddit_scraper.database.models.post import Post
from video_editor.director.short_video_format_config import ShortVideoFormatConfig


class Director:
    """
    Default implementation for the clip director.
    This class is responsible for creating the individual clips.
    """

    def __init__(self, tts_generator, image_generator, director_algorithm):
        """
        Ctor takes the following parameters:
        :param tts_generator: text-to-speech generator - responsible for generating text-to-speech audio
        :param image_generator: image generator is responsible for generating images for posts
        :param director_algorithm: director algorithm is responsible for picking out the comments that
        are meant to be included in the video
        """
        self._tts_generator = tts_generator
        self._image_generator = image_generator
        self._director_algorithm = director_algorithm

    def create_short_video(self, post: Post, format_config: ShortVideoFormatConfig):
        """
        Creates a short-format video for the given post
        :param post: post to be processed
        :param format_config: format for the video
        :return:
        """
