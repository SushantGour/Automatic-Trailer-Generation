# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 13:57:27 2021

@author: Sushant Gour
"""


"""
This code merges the data of path1 and path2 into the merged_path.
"""
import os


""" Inputs """
# paths to the two folders whose contents we want to merge
path1 = "C:/Users/DELL/Desktop/Sushant Internship Project/JokerFaces"
path2 = "C:/Users/DELL/Desktop/Sushant Internship Project/JokerScenesWithoutClashes"
# path where we want to store the merged data.
merged_path = "C:/Users/DELL/Desktop/Sushant Internship Project/JokerFinalScenes"


# merge contents of the two folders
filenames=[]
folder = os.fsencode(path1)


for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames.append(filename)
        
        
for i in range(len(filenames)):
    file=filenames[i]
    src= path1 + "/" + file
    dest= merged_path + "/" + file
    os.rename(src, dest)
    
    
filenames1=[]
folder1=os.fsencode(path2)
for file in os.listdir(folder1):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames1.append(filename)
        
        
for i in range(len(filenames1)):
    file=filenames1[i]
    src= path2 + "/" + file
    dest= merged_path + "/" + file
    os.rename(src, dest)