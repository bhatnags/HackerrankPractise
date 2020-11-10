import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'moviepy'])

# import the lib
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

start_time = 1*60
end_time = 10*60

# this will take the LiveC
ffmpeg_extract_subclip("inputvideo.mp4", start_time, end_time, targetname="outputvideo.mp4")
