"""
This code file is used to add the theme music file (mp3) as a background music
int the trailer file (mp4). The output of this code is the final trailer (mp4)
having theme music in its background.
"""


import os


# This method uses a direct ffmpeg call to add background music to a video.
# It merges the audio already present in the video with the background
# audio and hence, the duration of the final audio will be equal to the 
# smaller duration among the two audios. This is done by the "shortest" keyword
# in the command.


""" Inputs """
# The path where the trailer and the Theme Music are located.
source_path = r"C:/Users/DELL/Desktop/Sushant Internship Project/JokerTrailerPlusThemeMusic"
os.chdir(source_path)
# name of the Theme Music file
theme_music="JokerThemeFinal.mp3_2x.mp3"
# Name of the trailer (without BGM)
input_video_name="JokerTrailerWithoutBGM.mp4"
# Name of the final trailer after adding BGM
output_file_name="FinalJokerTrailerWithBGM.mp4"

s1="ffmpeg -i"
s2="-i"
s3='-filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest'



call= s1 + " " + input_video_name + " " + s2 + " " + theme_music + " " + s3 + " " + output_file_name
print(call)
os.system(call)
#call1= f'ffmpeg -i JusticeLeagueTrailer4x.mp4 -i finalTheme3x.mp3 -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest JusticeLeagueFinalTrailer.mp4'
#os.system(call1)