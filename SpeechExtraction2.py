#%%      
"""
Created on Sat Jun 19 11:33:44 2021

@author: DELL
"""

import os
import re
import librosa
import librosa.display
import soundfile # to read audio file
import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn import mixture
import warnings
warnings.filterwarnings('ignore')


"""
This file calculates the outlier scores of all the speech segments
which were extracted from the movie and sorts the segments in
descending order of their outlier scores and choose as much segments
from the top that fits inside the duration of speech we need in the trailer
After that for the above chosen most impressive speech segments it extracts the corresponding
scenes from the original movie and stores them in the output_folder.


Input: The inputs to this file are:
    (1) path : path to the folder where all the speech segments which were extracted
        from the movie using SpeechExtraction1 are stored.
    (2) movie_path : the path to the movie file (mp4) from which we will
        extract the scenes corresponding to the most impressive speeches.
    (3) output_folder : the path of the folder where all the extracted
        impressive speeches will get stored.
    (4) totalDuration : it is the maximum duration of speeches which we
        can add in our trailer.
    (5) lowerThreshold : it is the lower limit on the length of an output speech segment
        to be able to get included in our trailer
    (6) upperThreshold : it is the upper limit on the length of an output speech segment
        to be able to get included in our trailer
        
Output: The output of this code is the most impressive speech segments (mp4)
        extracted from the movie which fits inside the duration of speech we
        want in our trailer. All the files (mp4) gets stored in the output_folder.
"""


""" Inputs """
# path variable contains the path to the folder where the extracted speech segments
# are stored.
path = "C:/Users/DELL/Desktop/Sushant Internship Project/extractedSpeeches"
# movie_path contains the path to the movie from which we will extract
# clips corresponding to the top outlier scores.
movie_path="C:/Users/DELL/Desktop/Sushant Internship Project/JokerReal.mp4"
# output_folder is the path where we will extract the most impressive speeches.
output_folder= "C:/Users/DELL/Desktop/Sushant Internship Project/SpeechesOfJoker"
os.chdir(output_folder)

# beow is the maximum duration of speech we want in the trailer in seconds.
# here i have set is as 40% of a 3 minute (180 seconds) trailer
totalDurationOfSpeech=180*0.4

# Constraints on the length of the speech segments
lowerThreshold=3
upperThreshold=10


folder = os.fsencode(path)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.wav') ): # whatever file types you're using...
        filenames.append(filename)
filenames.sort()


noOfFramesList= []
scoreList= []
finalAudioFeatures= [[]]
count=0

# The below code extracts the featires from the speeches and calculates
# their outlier scores.
for i, file in enumerate(filenames):
    audio_file = path+"/"+filenames[i]
    ipd.Audio(audio_file)
    # load audio files with librosa
    signal, sr = librosa.load(audio_file)
    
    
    mfccs = librosa.feature.mfcc(y=signal, n_mfcc=13, sr=sr)
    
    
    delta_mfccs = librosa.feature.delta(mfccs)
    delta2_mfccs = librosa.feature.delta(mfccs, order=2)
    
    
    mfccs_features = np.concatenate((mfccs, delta_mfccs, delta2_mfccs))


    melSpectogram=librosa.feature.melspectrogram(y=signal, sr=sr)


    melSpectogram_db = librosa.power_to_db(melSpectogram, ref=np.max)





    # We will take hop_length according to the below formula:
    # No of Frames= ((Samples-FrameSize)/HopSize)  + 1
    # Here, no of samples are found by signal.shape
    # FrameSize = 1 Sample in a wav file
    # we want no of frames same as the no of frames in the MFCC vector so that we can concatenate both
    # Hence, No of Frames = 1445
    # On Solving, HopSize comes out to be 511.645675, Hence, we take it as 512


    # chroma vector using signal and sr as inputs
    hop_length=512
    chromagram = librosa.feature.chroma_stft(signal, sr=sr, hop_length=hop_length)


    # chroma vector using power spectrogram/mel spectogram as input
    chromagramReal = librosa.feature.chroma_stft(signal, sr=sr, S=melSpectogram_db)
    #print(chromagramReal.shape)
    

    samplesPerFrame= 512
    nFrames= math.ceil(len(signal)/samplesPerFrame)
    noOfFramesList.append(nFrames)



     




    audio_features = np.concatenate((mfccs, delta_mfccs, chromagramReal))


    # Now, audio features has size 25 * nFrames, but, GaussianMixture takes the feature vector
    # in such a form that the coloumns represents the different features and the rows represents
    # the different data points. In our case, each data point is a frame which has a feature
    # vector associated with it. Hence, we have to take the transpose of audio_features array
    # so that it comes in the form where each row index represents each frame or data point and
    # each coloumn index represents a feature. i.e., each row is a feature vector of the corresponding
    # frame or data point.


    # Taking transpose of audio_features and storing it in a new array named as audioFeaturesReal. 
    audioFeaturesReal = [[0 for x in range(38)] for y in range(nFrames)]
    for i in range(nFrames):
            for j in range(38):
                audioFeaturesReal[i][j] = audio_features[j][i]
    if count==0:
        finalAudioFeatures = [[0 for x in range(38)] for y in range(nFrames)]
        for i in range(nFrames):
                for j in range(38):
                    finalAudioFeatures[i][j] = audioFeaturesReal[i][j]
        count= count + 1
    else:
        finalAudioFeatures= np.concatenate((finalAudioFeatures,audioFeaturesReal))


# Training the GMM Model on the audioFeaturesReal array.


# Fitting GMM on our audioFeaturesReal array.
model = mixture.GaussianMixture(n_components = 16, max_iter = 200, covariance_type='diag', reg_covar=1e-01, n_init = 3)
model.fit(finalAudioFeatures)
gmmOutput= model.score_samples(finalAudioFeatures)


prev=0
for i in range(len(noOfFramesList)):
    sum=0
    for j in range(noOfFramesList[i]):
        sum= sum + gmmOutput[prev+j]
    score=((-1)* sum)/noOfFramesList[i]
    scoreList.append(score)
    prev=noOfFramesList[i]


# calculating the deviation from the mean score:
# The outlier score is actually the deviation
# from the mean score. That is, the segments having
# the largest deviation from the mean score will be the
# most impressive segment as the mean score represents the
# normal speeches. 
outlierScore=[]
mean=0


for i in range(len(scoreList)):
    mean = mean + scoreList[i]


mean = mean/len(scoreList)

for i in range(len(scoreList)):
    x = mean - scoreList[i]
    if(x<0):
        x = (-1)*x
    outlierScore.append(x)



filenamePlusOutlierScore= []
for i in range(len(outlierScore)):
    pair= (filenames[i],outlierScore[i])
    filenamePlusOutlierScore.append(pair)


# Sorting filenamePlusOutlierScores w.r.t. the Outlier Scores


def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    return(sorted(tup, key = lambda x: x[1], reverse=True))



finalListSortedOutlierScore= Sort_Tuple(filenamePlusOutlierScore)

    
    


#%%
# This code extracts the most impressive speech segments from the movie
# in the form of mp4 files.
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


count=0
for i in range(len(finalListSortedOutlierScore)):
    File=finalListSortedOutlierScore[i][0]
    timestamps=re.findall(r'[\d\.\d]+', File)
    timestamp0=float(timestamps[0])
    timestamp1=float(timestamps[1])
    if(count+(timestamp1-timestamp0)<=totalDurationOfSpeech):
        # Export this file
        if(timestamp1-timestamp0>=lowerThreshold and timestamp1-timestamp0<=upperThreshold):
                 ffmpeg_extract_subclip(movie_path, timestamp0, timestamp1, targetname= "("+ str(timestamp0)+","+ str(timestamp1)+").mp4")
                 count+=(timestamp1-timestamp0)
    else:
        continue
    
    
print(totalDurationOfSpeech-count)