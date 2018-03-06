import os
from google.cloud import speech

a = os.listdir()

if a:
    try:
        print("hello")
    except Exception as ex:
        print(ex)
else:
    print("hello")
