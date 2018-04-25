import os
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\projects\\roehakol\\speech-api\\RoeHaKol-96254847b7fb.json"
GCS_URI = "gs://roehakol-speech/rav-sherki-hordos.flac"


def long_running_recognize(gcp_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=GCS_URI)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        # sample_rate_hertz=16000,
        language_code='he-IL')

    started_recognition = time.time()
    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result()
    print(time.time() - started_recognition)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    return response


def resolve_speech_response(response, destination):
    list_of_transcripts = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        list_of_transcripts.append(bytearray(result.alternatives[0].transcript, "utf-8"))
        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        # print('Confidence: {}'.format(result.alternatives[0].confidence))
    with open(destination, mode="ab") as f:
        f.writelines(list_of_transcripts)


res = long_running_recognize(GCS_URI)
resolve_speech_response(res, "lesson.txt")
