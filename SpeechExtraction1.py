"""
Created on Thu Jun 24 16:39:18 2021

@author: Sushant Gour
"""

"""
This file is used for transcribing speech in a whole movie and extracting the
resulting speech segments.
The libraries used are: io, videointelligence_v1, os, pydub, pathlib and moviepy.

Inputs: The inputs required in this file are:
    (1) video_path: It is the path to the video file representing the movie (mp4)
    (2) audio_path: the path to the audio file that contains the audio of the movie.
    (3) output_path: the output directory where all the extracted speech segments will get
          stored.
    (4)	x: it is a number between 0 and 100 which represents the percentage of speech from the 
    start that we are considering. This threshold is used to avoid spoilers as spoilers are 
    generally present towards the end of the movie. The ideal value for x is 80.
    (5)	language_code: It is the language code of the language in the movie. The language 
    codes can be found from GCP platform. For American English, the code is: en-US.

    
Output: The output of this file is all the speech segments which lies inside the
        first x% of the speeches in the movie.The last (100-x)% speeches are not extracted
        as they might contains spoilers. The output format of the speech segments is "wav".
        The output file names itself contains the timestamps of the corresponding speech segments
        in the movie in seconds. The output file names have the following
        format: (startTime,endTime).wav where startTime and endTime are in seconds. The output
        files gets stored in the output_path directory.
"""


import io
#from google.cloud import videointelligence
from google.cloud import videointelligence_v1 as vi
import os
from pathlib import Path


# Set the Google_Application_Credentials to the path of the JSON file
# downloaded from the Google Cloud Platform.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/DELL/Downloads/serious-sublime-315717-d0105be08d39.json"


""" Inputs """
# path variable stores the path to the video which we are transcribing.
video_path="C:/Users/DELL/Desktop/Sushant Internship Project/JokerCompressed.mp4"
# audio_path stores the path to the audio file which contains the audio of the whole movie.
audio_path = Path("C:/Users/DELL/Desktop/Sushant Internship Project/JokerReal.mp3")
# language code of the language used in the movie.
language_code = "en-US"
# x is the percentage of speech we are considering from the start of the movie.
x=80
# Below is the path where all the output is extracted.
output_path = "C:/Users/DELL/Desktop/Sushant Internship Project/extractedSpeeches"
os.chdir(output_path)


# Getting the duration of the movie in seconds
from moviepy.editor import VideoFileClip
clip = VideoFileClip(video_path)
movie_duration=clip.duration
print(movie_duration)


with io.open(video_path, "rb") as file:
    input_content = file.read()


# Below code is for transcribing speech from the input video.
# The variable lastWordTime stores the timestamp of the last word occuring in the video.
lastWordTime=0
def transcribe_speech(input_content, language_code, segments=None):
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.SPEECH_TRANSCRIPTION]
    config = vi.SpeechTranscriptionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    context = vi.VideoContext(
        segments=segments,
        speech_transcription_config=config,
    )
    
    print(f"Processing video: {video_path}...")
    operation = video_client.annotate_video(
    request={"features": features, "input_content": input_content,"video_context": context}
    )
    return operation.result(timeout=10000)


from datetime import timedelta


segment = vi.VideoSegment(
    start_time_offset=timedelta(seconds=0),
    end_time_offset=timedelta(seconds=movie_duration), 
    # end_time_offset should be greater than or equal
    # to the length of the movie in seconds as start_time_offset and end_time_offset
    # represents part of the movie which will be transcribed. As we want the whole
    # movie to be transcribed, set start_time_offset=0 and end_time_offset= length of the movie
    # in seconds.
)

response = transcribe_speech(input_content, language_code, [segment])

def print_video_speech(response,lastWordTime,min_confidence=0.7):
    def keep_transcription(transcription):
            return min_confidence <= transcription.alternatives[0].confidence
    
    segmentValues= []
    # First result only, as a single video is processed
    transcriptions = response.annotation_results[0].speech_transcriptions
    transcriptions = [t for t in transcriptions if keep_transcription(t)]

    print(f" Speech Transcriptions: {len(transcriptions)} ".center(80, "-"))
    fullstop= '.'
    for transcription in transcriptions:
        best_alternative = transcription.alternatives[0]
        confidence = best_alternative.confidence
        transcript = best_alternative.transcript
        start= 0
        end=0
        flag=0
        for word in best_alternative.words:
            t1 = word.start_time.total_seconds()
            t2 = word.end_time.total_seconds()
            lastWordTime=t2
            if flag==0 :
                start=t1
            end= t2 + 0.5                 # Can make it t2+1
            flag= flag + 1
        print(f" {confidence:4.0%} | {transcript.strip()}")
        pair = (start, end)
        if((end-start<=20) and len(best_alternative.words)>=5):
            segmentValues.append(pair)
        y=0
        # Breaking a speech segment about a fullstop lying near the middle of 
        # the speech segment if length of the speech segment
        # is greater than 20 seconds.
        if((end-start)>20 and (end-start)<=40 and len(best_alternative.words)>=10):
            x= (int)(start+end)/2
            for word in best_alternative.words:
                t1 = word.start_time.total_seconds()
                t2 = word.end_time.total_seconds()
                if(word.word[len(word.word)-1]==fullstop and t2<=x):
                    y=t2 + 0.5
            if(y==0):
                for word in best_alternative.words:
                    t1 = word.start_time.total_seconds()
                    t2 = word.end_time.total_seconds()
                    if(word.word[len(word.word)-1]==fullstop):
                        y=t2 + 0.5
                        break
            # The case when there is no fullstop at all in the transcript.
            if(y!=0):
                pair1=(start,y)
                segmentValues.append(pair1)
                if(y+1<end):
                    pair2=(y+1,end)
                    segmentValues.append(pair2)
                    print(pair1,"and",pair2)
            else:
                segmentValues.append(pair)
                
            
    return segmentValues,lastWordTime


segmentValues,lastWordTime= print_video_speech(response,lastWordTime,0.7)
print(len(segmentValues))
print(segmentValues)
print(lastWordTime)


# Segmenting a Video based on the segmentValues array obtained above:
    
    
#Extracting audio files in the corresponding shots
# We only extract the speech segments which lies inside the first x% of the
# speech in the movie. The last (100-x)% speech is not extracted to avoid spoilers.


from pydub import AudioSegment
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



# The variable timeOfLastConsideredWord stores the last word till which we
# will extract the speech. Here, we set it as the first x% of the speech in the movie.
timeOfLastConsideredWord= ((lastWordTime)*(x/100))
print(timeOfLastConsideredWord)


# set the path of the ffmpeg files that we downloaded from the ffmpeg's website
# under the variables given below. This will allow us to use the ffmpeg tool
# for audio and video processing.
AudioSegment.converter = "C:/Users/DELL/Desktop/Sushant Internship Project/ffmpeg.exe"
AudioSegment.ffprobe   = "C:/Users/DELL/Desktop/Sushant Internship Project/ffprobe.exe"




# The below code is to extract the speech segments which lie inside the first x%
# of the movie
for i,  pair in enumerate(segmentValues):
    # Time to miliseconds
    startTime = segmentValues[i][0]*1000
    endTime = segmentValues[i][1]*1000
    if(startTime<endTime and segmentValues[i][1]<=timeOfLastConsideredWord):
        ffmpeg_extract_subclip(audio_path, startTime/1000, endTime/1000, targetname= "("+ str(startTime/1000)+","+ str(endTime/1000)+").wav")


