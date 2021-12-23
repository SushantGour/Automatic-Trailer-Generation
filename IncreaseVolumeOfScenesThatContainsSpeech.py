#%%
""" CELL-01 """
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 16:39:18 2021

@author: Sushant Gour
"""


"""
This code moves the files containing speech in them to an intermediate folder, increases their 
volume and then again move back the files to the source folder.
"""

import io


#from google.cloud import videointelligence
from google.cloud import videointelligence_v1 as vi
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/DELL/Downloads/serious-sublime-315717-d0105be08d39.json"


""" Inputs """
# Path to the source folder
source_path="C:/Users/DELL/Desktop/Sushant Internship Project/JokerFinalScenes"
# Path to the intermediate folder
intermediate_path= "C:/Users/DELL/Desktop/Sushant Internship Project/yesSpeech"
# It is the language code for the language used in the movie.
language_code = "en-US"
# The factor by which we want to increase the volume.
volume=4
volume=str(volume)



# Check which files contain speech using Speech Transcription and move them to the
# intermediate folder.
folder = os.fsencode(source_path)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames.append(filename)
print(filenames)

for filename in filenames:
    with io.open(source_path + "/" + filename, "rb") as file:
        input_content = file.read()




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
    
        print(f"Processing video: {source_path}...")
        operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content,"video_context": context}
        )
        return operation.result(timeout=10000)
    

    from datetime import timedelta

    
    segment = vi.VideoSegment(
        start_time_offset=timedelta(seconds=0),
        end_time_offset=timedelta(seconds=7205),
    )

    response = transcribe_speech(input_content, language_code, [segment])

    def print_video_speech(response, min_confidence=0.8):
        def keep_transcription(transcription):
            return min_confidence <= transcription.alternatives[0].confidence
    
        
        # First result only, as a single video is processed
        transcriptions = response.annotation_results[0].speech_transcriptions
        #transcriptions = [t for t in transcriptions if keep_transcription(t)]

            
        print(f" Speech Transcriptions: {len(transcriptions)} ".center(80, "-"), str(filename))
        if(len(transcriptions)>0):
            return True
        else:
            return False
        
       
    if(print_video_speech(response,0.8)==True):
        newFilename= filename
        src= source_path + "/" + filename
        dest= intermediate_path + "/" + newFilename
        os.rename(src, dest)


#%%
os.chdir(intermediate_path)


# increase volume of all files in the intermediate folder.
call= "for /r %i in (*.mp4) do ffmpeg -i" + " " + '"%i"' + " " + '-filter:a "volume=' + volume + '"' + " " + '"%i_Amplified.mp4"'
#call= f'for /r %i in (*.mp4) do ffmpeg -i "%i" -filter:a "volume=2.0" "%i_Amplified.mp4"'
os.system(call)


#%%
# After amplifying all the files in the intermediate folder, delete the old files
# The new amplified files have the suffix "Amplified" in their names.
# Hence, delete all the files that don't have the "Amplified" suffix in them.
folder1 = os.fsencode(intermediate_path)

filenames1 = []

for file in os.listdir(folder1):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames1.append(filename)
        
        
for i in range(len(filenames1)):
    file=filenames1[i]
    if(file.find("Amplified")==-1):
        os.remove(file)
     
        
# moving the amplified files back to the source folder.        
filenames2=[]
folder2 = os.fsencode(intermediate_path)



for file in os.listdir(folder2):
    filename = os.fsdecode(file)
    if filename.endswith( ('.mp4') ): # whatever file types you're using...
        filenames2.append(filename)
        
        
for i in range(len(filenames2)):
    file=filenames2[i]
    src= intermediate_path + "/" + file
    dest= source_path + "/" + file
    os.rename(src, dest)