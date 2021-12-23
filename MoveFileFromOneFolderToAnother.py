"""
This code is used to move a file from one folder to another.
"""
import os

# path to the source folder
source_path= "C:/Users/DELL/Desktop/Sushant Internship Project/JokerFinalScenes"
# path to the destination folder
destination_path="C:/Users/DELL/Desktop/Sushant Internship Project/JokerTrailerPlusThemeMusic"
# name of the file to be moved
filename="JokerTrailerWithoutBGM.mp4"



# Move the file from source_path to destination_path
src= source_path + "/" + filename
dest= destination_path + "/" + filename
os.rename(src, dest)