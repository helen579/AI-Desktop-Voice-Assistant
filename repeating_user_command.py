import speech_recognition as sr
import  time
import os
from gtts import gTTS
import tempfile
import pygame


def say(phrase):
    tts = gTTS(text=phrase, lang="en")
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as f:
        tmpfile = f.name
        print(tmpfile)
    tts.save(tmpfile)
    play_mp3(tmpfile)
    os.remove(tmpfile)


def play_mp3(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes: # this version of Python uses bytes for strings (Python 2)
                say(phrase=format(value).encode("utf-8"))
            else: # this version of Python uses unicode for strings (Python 3+)
                say("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        time.sleep(0.5) # sleep for a little bit
except KeyboardInterrupt:
    pass