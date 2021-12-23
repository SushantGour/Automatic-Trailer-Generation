"""
This code concatenates all the mp4 files in the source folder to make
a resultant mp4 file which is the trailer itself. The trailer gets created in the
source directory itself.
"""


import os
import re
# Import everything needed to edit video clips
from moviepy.editor import *


""" Inputs """
# path to the source folder
source_path = r"C:/Users/DELL/Desktop/Sushant Internship Project/JokerFinalScenes"
os.chdir(source_path)
# the name that we want to give to the trailer.
trailerName="JokerTrailerWithoutBGM.mp4"


# convert all mp4 files in the source directory to ts files.
call= f'for /r %i in (*.mp4) do ffmpeg -i "%i" -c copy -bsf:v h264_mp4toannexb -f mpegts "%i.ts"'
os.system(call)


# Making a text file containing names of the ts files line by line with format: file 'name'


folder = os.fsencode(source_path)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.ts') ): # whatever file types you're using...
        filenames.append(filename)




""" Below code is to sort the list of folders numerically (in chronological order) """
# It works similar to sort(arr,arr+n,compare) in C++.
# Here, the Compare function takes two strings s1 and s2 as input,
# extract the list of floats in the strings and store them in w and z
# and then compares w and z. For e.g. : s1="(123.33,127.7") and s2="(130, 134.7)",
# then w=[123.33,127.7] and z=[130,134.7]. Now, we compare first two elements of
# w and z to tell which string is smaller. If s1 is smaller, then swap s1 and s2.
import re

def compare(s1,s2):
    x=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", s1)
    y=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", s2)
    w=[float(c) for c in x]
    z=[float(c) for c in y]
    if(w[0]<z[0]):
        return True
    elif(w[0]>z[0]):
        return False
    else:
        if(w[1]<z[1]):
            return True
        else:
            return False
def sort_human(arr):
    n=len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if compare(arr[j + 1],arr[j]) :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]    
    return arr


# sort filenames according to chronological order
sort_human(filenames)


def save_flist(files):
    f_data = 'file \'' + '\'\nfile \''.join(files) + '\''
    print(f_data)

    f_list = 'list.txt'
    with open(f_list, 'w', encoding='gbk') as f:
        f.write(f_data)
    return f_list


# f_list is a text file containin the names of all ts files in
# chronoligical order. It contains one name per line.
f_list = save_flist(filenames)


# Below Code is for concatenating a set of mp4 files together
# Run this to concatenate all ts files an convert the resulting file back to mp4 file.
call1= f'ffmpeg -f concat -safe 0 -i {f_list} -c copy -bsf:a aac_adtstoasc {trailerName} -y'


os.system(call1)