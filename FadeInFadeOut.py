# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 18:32:23 2021

@author: DELL
"""

"""
This code is used to apply fade in and fade out effect to all the scenes that are to be stitched 
together. I assume that we have all the scenes on which we want to apply fade in and fade out effect 
in a folder.


Tool used: ffmpeg


The inputs and outputs of this file are given below:
    
    
Inputs: This file requires the following inputs:
(1)	path: This variable stores the path to the folder that contains all those scenes on which we want 
to add fade in and fade out effect.
(2)	fadeDuration: This is the fade duration in seconds which we want to apply. A fade in effect of 
length = fadeDuration and a fade out effect of length = fadeDuration will be applied to each scene. 
The fade in and fade out effects are applied to both the video and the audio of a particular scene.


Output: For each file in the “path” folder, a new file is created which is having fade in and fade out 
effect in it. The name of the new file is = oldFileName + “_WithFadeIn”.
Now, at the end of the code, we delete all the old files from the “path” directory and hence, only 
the new files which have fade in and fade out effects in them are left in the “path” directory.
"""
import os
import re
import cv2
from moviepy.editor import *


""" Inputs """
# path to the folder where all the scenes are located
path = r"C:/Users/DELL/Desktop/Sushant Internship Project/JokerFaces"
os.chdir(path)
# fade duration
fadeDuration=0.2
fadeDuration=str(fadeDuration)


s1="for /r %i in (*.mp4) do ffmpeg -i"
s2='"%i"'
s3="-filter_complex"
s4='"'
s5="fade=d="
s6=", reverse, fade=d="
s7=", reverse; afade=d="
s8=", areverse, afade=d="
s9=", areverse"
s10='"%i_WithFadeIn.mp4"'
call= s1+" "+s2+" "+s3+" "+s4+s5+fadeDuration+s6+fadeDuration+s7+fadeDuration+s8+fadeDuration+s9+s4+" "+s10


#call= f'for /r %i in (*.mp4) do ffmpeg -i "%i" -filter_complex "fade=d=0.5, reverse, fade=d=0.5, reverse; afade=d=0.5, areverse, afade=d=0.5, areverse" "%i_WithFadeIn.mp4"'


os.system(call)


# deleting the old files and keeping only the new files having fade in and fade out
# effects in them.
folder = os.fsencode(path)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames.append(filename)
        
        
for i in range(len(filenames)):
    file=filenames[i]
    if(file.find("WithFadeIn")==-1):
        os.remove(file)