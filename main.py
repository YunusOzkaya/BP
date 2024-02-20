"""from gtts import gTTS
from io import BytesIO
import pygame
import speech_recognition as sr
import wikipedia
import time


def speak(text, lang):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fo)
    return mp3_fo


def text_to_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bir şeyler söyleyin...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="tr")
            print("Google şunu dediğini düşünüyor:\n" + text)
            return text
        except:
            print("Söyleneni anlayamadım, lütfen tekrar deneyin.")
            play_sound("Söyleneni anlayamadım, lütfen tekrar deneyin.")
            return text_to_speech()


def play_sound(text):
    sound = speak(text, "tr")
    sound.seek(0)
    pygame.mixer.init()
    sound_obj = pygame.mixer.Sound(sound)
    sound_obj.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)


def search_wikipedia(query):
    wikipedia.set_lang("tr")
    try:
        result = wikipedia.summary(query, sentences=4)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        result = wikipedia.summary(e.options[0], sentences=4)
        return result
    except wikipedia.exceptions.PageError:
        return "Wikipedia'da bu konuyla ilgili bir sayfa bulunamadı."


stop_word = "bitir lan"
while True:
    word = text_to_speech()
    if word == stop_word:
        break
    wikipedia_result = search_wikipedia(word)
    print("Wikipedia Sonucu:")
    print(wikipedia_result)
    play_sound(wikipedia_result)"""

from flask import Flask, render_template, request
from gtts import gTTS
from io import BytesIO
import pygame
import speech_recognition as sr
import wikipedia
import time

app = Flask(__name__)


def speak(text, lang):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fo)
    return mp3_fo


def play_sound(text):
    sound = speak(text, "tr")
    sound.seek(0)
    pygame.mixer.init()
    sound_obj = pygame.mixer.Sound(sound)
    sound_obj.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)


def search_wikipedia(query):
    wikipedia.set_lang("tr")
    try:
        result = wikipedia.summary(query, sentences=4)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        result = wikipedia.summary(e.options[0], sentences=3)
        return result
    except wikipedia.exceptions.PageError:
        return "Wikipedia'da bu konuyla ilgili bir sayfa bulunamadı."


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "search" in request.form:
            query = request.form["search"]
            wikipedia_result = search_wikipedia(query)
            play_sound(wikipedia_result)
            return render_template("index.html", wikipedia_result=wikipedia_result)
    else:
        text = voice_to_text()
        if text:
            wikipedia_result = search_wikipedia(text)
            play_sound(wikipedia_result)
            return render_template("index.html", wikipedia_result=wikipedia_result)
    return render_template("index.html")


def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bir şeyler söyleyin...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="tr")
            print("Google şunu dediğini düşünüyor:\n" + text)
            return text
        except:
            print("Söyleneni anlayamadım, lütfen tekrar deneyin.")
            return None


if __name__ == "__main__":
    app.run(debug=True)
