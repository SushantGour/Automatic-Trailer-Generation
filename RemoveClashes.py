"""
This code traverses in the source folder and if a file doesn't have clash with any other file,
then it moves that file to the destination folder. If some files have clashes, then, it discards
them and extracts their union from the movie and stores it in the destination folder.
For ex: say three files have clashes: (10,15), (12,17) ,(15,20), then it discards all the
three files and extracts their union i.e. (10,20) from the movie and stores it in the destination
folder.
"""


import os
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


""" Inputs """
# Path to the source folder
source= "C:/Users/DELL/Desktop/Sushant Internship Project/JokerScenes" # path to the folder containing all extracted clips for the trailer.
# Path to the destination folder
destination= "C:/Users/DELL/Desktop/Sushant Internship Project/JokerScenesWithoutClashes" # path to the folder where all the final clips after merging overlapping clips will be stored.
os.chdir(destination)
# Path to the movie
movie_path="C:/Users/DELL/Desktop/Sushant Internship Project/JokerReal.mp4"


folder = os.fsencode(source)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames.append(filename)


""" Below code is to sort the list of folders numerically"""
# Numerically means that the files are sorted in ascending
# order of their timestamps. For ex: (10.7,15.2) will come before (20.5,30.3)
# in the ordering If start time is same, then the ordering is done w.r.t. the end time.
# It works similar to sort(arr,arr+n,compare) in C++.
# Here, the Compare function takes two strings s1 and s2 as input,
# extract the list of floats in the strings and store them in w and z
# and then compares w and z. For e.g. : s1="(123.33,127.7") and s2="(130, 134.7)",
# then w=[123.33,127.7] and z=[130,134.7]. Now, we compare first two elements of
# w and z to tell which string is smaller. If s1 is smaller, then swap s1 and s2.

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


# sort the filenames array in ascending order of the timestamps of the files.
sort_human(filenames)


# Remove Clashes
i=0
while i<(len(filenames)-1):
    currFile=filenames[i]
    x=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", currFile)
    timestamp0=float(x[0])
    timestamp1=float(x[1])
    nextFile=filenames[i+1]
    y=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", nextFile)
    timestamp2=float(y[0])
    timestamp3=float(y[1])
    if(timestamp2>=timestamp1):
        newFilename= currFile
        src= source + "/" + currFile
        dest= destination + "/" + newFilename
        os.rename(src, dest)
        if(i==len(filenames)-2):
            newFilename= nextFile
            src= source + "/" + nextFile
            dest= destination + "/" + newFilename
            os.rename(src, dest)
        i+=1
    else:
        start=timestamp0
        end=0
        if(timestamp1>timestamp3):
            end=timestamp1
        else:
            end=timestamp3
            
        if(i==len(filenames)-2):
            ffmpeg_extract_subclip(movie_path,start,end,targetname="("+ str(start)+","+ str(end)+ ").mp4")
        else:
            while timestamp2<timestamp1 and i<(len(filenames)-1):
                if(timestamp1>timestamp3):
                    end=timestamp1
                else:
                    end=timestamp3
                if(i==len(filenames)-2):
                    i+=1
                    break
                i+=1
                currFile1=filenames[i]
                x1=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", currFile1)
                timestamp0=float(x1[0])
                timestamp1=float(x1[1])
                nextFile1=filenames[i+1]
                y1=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", nextFile1)
                timestamp2=float(y1[0])
                timestamp3=float(y1[1])
            ffmpeg_extract_subclip(movie_path,start,end,targetname="("+ str(start)+","+ str(end)+ ").mp4")
            i+=1
            if(i==len(filenames)-1):
                currFile=filenames[i]
                newFilename= currFile
                src= source + "/" + currFile
                dest= destination + "/" + newFilename
                os.rename(src, dest)