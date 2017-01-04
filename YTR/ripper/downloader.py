# Python imports
import os
from urllib import parse
from subprocess import run
# Dependencies
from youtube_dl import YoutubeDL
# Project Imports
from YTR.ripper import file_helpers


class YTRLogger(object):
    def debug(self, msg):
        print('\nDegug -> ', msg, '  From: ', self)

    def warning(self, msg):
        print('\nWarning -> ', msg, '  From: ', self)

    def error(self, msg):
        print('Error:', msg, '  From: ', self)


# Get the name of the video (song)
def get_name(my_url):
    with YoutubeDL({'outtmpl': '%(title)s'}) as ydl:
        video_info = ydl.extract_info(my_url, download=False)
        video_name = video_info.get('title', None)
    return my_url, video_name


# download self.link
class Dl(object):

    def __init__(self, link, name):
        self.link = link
        self.name = name

    def song_dl(self):
        """
            If you would like to change download options, pass options to YoutubeDL
            Example from youtube-dl Docs:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'logger': MyLogger(),
                    'progress_hooks': [my_hook],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([str(self.link)])

            All options can be found at:  https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
        """
        # To change download options, pass a dict to YoutubeDL()
        #  Example:
        with YoutubeDL() as ydl:
            ydl.download([str(self.link)])

    # Convert video to MP3
    def convert_song(self):
        # Find this video, rename it w/ os.quote_plus
        my_video = file_helpers.find_song(which_dir=os.getcwd(),
                                          song_name=self.name)
        # Rename video to prevent FFmpeg errors
        os.rename(my_video, parse.quote_plus(my_video))

        # Get the video name + its extension
        vid_name, vid_ext = os.path.splitext(my_video)

        # Convert the song w/ FFmpeg
        run('ffmpeg -i "%s" -vn -ar 44100 -ac 2 -ab 200k -f mp3 "%s".mp3 | ffmpeg'
            % (parse.quote_plus(my_video), vid_name),
            shell=True)

        # Get video
        mv = file_helpers.find_song(which_dir=os.getcwd(),
                                    song_name=parse.quote_plus(my_video))
        # Music folder == cwd -> YTR -> static -> music
        # Move video
        music_folder = os.path.join(os.getcwd(), "YTR", "static", "music")
        os.rename(mv, os.path.join(music_folder, mv))
        # Remove video
        os.remove(os.path.join(music_folder, mv))
        # Get Song
        my_song = file_helpers.find_song(which_dir=os.getcwd(),
                                         song_name=self.name)
        song_name, song_ext = os.path.splitext(my_song)
        # Move song
        os.rename(my_song, os.path.join(music_folder, str(self.name + song_ext)))
        return file_helpers.find_song(os.path.join(os.getcwd(), "YTR", "static", "music"),
                                      song_name=self.name)


def my_test():
    northlane = "https://www.youtube.com/watch?v=IjMuhtDkN7o"
    north_link, north_name = get_name(northlane)
    north_video = Dl(north_link, north_name)
    north_video.download()
    yield str(north_video.convert_song())
# my_test()
