"""Asynchronously transcribes the audio file specified by the gcs_uri."""

import os
import time
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\projects\\roehakol\\speech-api\\RoeHaKol-0f86b9fd98ed.json"
GCS_URI = "gs://roehakol-speech/dvora-10min.wav"

client = speech.SpeechClient()

audio = types.RecognitionAudio(uri=GCS_URI)
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='he-IL')

started_recognition = time.time()
operation = client.long_running_recognize(config, audio)

print('Waiting for operation to complete...')
response = operation.result()
print(time.time() - started_recognition)
# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    print('Confidence: {}'.format(result.alternatives[0].confidence))