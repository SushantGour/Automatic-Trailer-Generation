"""
This code file is used to extract horror scenes from a movie. The inputs and outputs of this file are 
given below:
    
    
Inputs: The file requires the following inputs:
(1)	audio_path: This variable stores the path to the audio (in wav format) of the movie. 
Note that this audio file should be of wav format.
(2)	totalDurationOfHorrorScenes: This variable represents the total duration of horror scenes we want 
in our trailer.
(3)	movie_path: This variable stores the path of the original movie (mp4) from which the horror scenes 
are to be extracted.
(4)	output_folder: This variable stores the path of the output folder in which the extracted horror 
scenes are going to get stored.


Output: The code extracts horror scenes from the movie and stores them in the output_path folder. 
All the horror scenes are having mp4 format. Also, the sum of all the horror scenes does not exceeds 
the total duration of horror scenes that we want in our trailer. The output files are having the 
names as: (startTime,endTime) where startTime is the starting time of that horror scene and endTime 
is the ending time of that horror scene in the movie.
"""


import librosa
import os


""" Inputs """
# path to the audio file of the movie (wav)
audio_path="C:/Users/DELL/Desktop/Sushant Internship Project/AnnabelleReal.wav"
# total duration of horror scenes that we want in our trailer
totalDurationOfHorrorScenes=180*0.2
# path to the movie file (mp4)
movie_path="C:/Users/DELL/Desktop/Sushant Internship Project/AnnabelleReal.mp4"
# path where the output is going to get stored
output_path = "C:/Users/DELL/Desktop/Sushant Internship Project/HorrorScenesOfAnnabelle"
os.chdir(output_path)


# Load the Audio File
x, sr = librosa.load(audio_path,sr=16000)

# Creating a window of 5 seconds
max_slice=5 
window_length = max_slice * sr

# Create an energy array that stores energy of each window
import numpy as np
energy = np.array([sum(abs(x[i:i+window_length]**2)) for i in range(0, len(x), window_length)])

# finding the maximum energy among all windows
maxEnergy=0
for i in range(len(energy)):
    if(energy[i]>maxEnergy):
        maxEnergy=energy[i]
        
        
thresh=0


import pandas as pd
df=pd.DataFrame(columns=['energy','start','end'])
row_index=0
for i in range(len(energy)):
  value=energy[i]
  if(value>=thresh):
    i=np.where(energy == value)[0]
    df.loc[row_index,'energy']=value
    df.loc[row_index,'start']=i[0] * 5
    df.loc[row_index,'end']=(i[0]+1) * 5
    row_index= row_index + 1
    

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
start=np.array(df['start']) # start array contains the starting time of all windows
end=np.array(df['end'])     # end array contains the ending time of all windows
val=np.array(df['energy'])  # val array contains the energies of all windows


finalArray=[]
for i in range(len(start)):
    tup=(start[i],end[i],val[i])
    finalArray.append(tup)
    
    
def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    return(sorted(tup, key = lambda x: x[2], reverse=True))


# sort the array in descending order of energies.
finalArrayReal=Sort_Tuple(finalArray)


# Extract as much Horror Scenes that fit inside the totalDurationOfHorrorScenes
# we want in our trailer.
count=0
startPointsTillNow=[]
for i in range(len(finalArrayReal)):
 start_lim=finalArrayReal[i][0]
 flag=0
  
 
 for j in range(len(startPointsTillNow)):
     if(start_lim<=startPointsTillNow[j]+60 and start_lim>=startPointsTillNow[j]-60):
         flag=1
         break
 

 end_lim   = finalArrayReal[i][1] 
 value=finalArrayReal[i][2] 
 if(count+(end_lim-start_lim)<=totalDurationOfHorrorScenes and flag==0):
     ffmpeg_extract_subclip(movie_path,start_lim,end_lim,targetname="("+ str(start_lim)+","+ str(end_lim)+ ").mp4")
     count+=(end_lim-start_lim)
     startPointsTillNow.append(start_lim)
 else:
     continue 