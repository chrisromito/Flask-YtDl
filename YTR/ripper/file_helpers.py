# Python imports
import os

# Dependencies
# import ffmpy
# Project imports
# from convert import convert.converter as converter
from YTR import convert


# Directory helpers
# -----------------#
# Current working directory
def get_cwd():
    return os.getcwd()


def music_dir():
    return os.path.join(os.getcwd(), "music/")


# Uses converter module to connect to FFmpeg && convert to mp3
def my_converter(infile):
    filename, file_extension = os.path.splitext(infile)
    better_outfile = str(filename + '.mp3')

    c = convert.converter.Converter(
        ffmpeg_path="ffmpeg"
        # ffmpeg_path=os.path.join(get_cwd(), "/YTR/convert/ffmpeg")
    )
    # Set the config for converter
    options = {
        'format': 'mp3',
        'audio': {
            'codec': 'mp3',
            'bitrate': '22050',
            'channels': 1
        }
    }
    conv = c.convert(infile=infile,
                     outfile=better_outfile,
                     options=options
                     )
    # return (x for x in conv)
    iter(conv)


# Check for video/mp3 files in current dir
def clean_dir():
    for filename in os.listdir(get_cwd()):
        if ".mkv" in filename[-4:]:
            os.rename(filename, "music/" + filename)
        elif ".mp4" in filename[-4:]:
            os.rename(filename, "music/" + filename)
        elif ".webm" in filename[-4:]:
            os.rename(filename, "music/" + filename)
            # print(filename, end='')
        elif ".mp3" in filename[-4:]:
            os.rename(filename, "music/" + filename)


# Check the cwd/music folder for non-MP3 files
# If a non-mp3 file exists, run it through converter
def soundcheck():
    for my_files in os.listdir(music_dir()):
        if ".mp3" not in my_files[-4:]:
            print(".mp3 is not in -> " + my_files)
            my_converter(my_files)
    # print(os.listdir(music_dir()))
