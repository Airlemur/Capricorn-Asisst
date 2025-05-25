#Maked by Airlemur
#Yardım ve destek için Osman_Rauf_Ucar (İnstagram dm)

import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import os
import webbrowser
from datetime import datetime
from colorama import Fore, init
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import pvporcupine
import pyaudio
import struct
import cohere
import re
import random

init(autoreset=True)

PORCUPINE_ACCESS_KEY = "YOUR_PORCUPINE_ACCESS_KEY"
OPEN_WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
SPOTIPY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
COHERE_API_KEY = "YOUR_COHERE_API_KEY"

WAKE_WORD = "hey google"

scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,user-read-recently-played"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

co = cohere.Client(COHERE_API_KEY)

#Metinleri bölerek sesin gecikmesini önlediğim fonksiyon.
def split_text_into_chunks(text, max_length):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


#Özellikle yapay zeka sohbet modu açıkken yazılan # * tarzındaki noktalama işaretlerinin okunmasını engellemek için kullandığım fonksiyon.
def clean_markdown(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **kalın** → kalın
    text = re.sub(r"__([^_]+)__", r"\1", text)     # __altı çizili__ → altı çizili
    text = re.sub(r"#\s*", "", text)              # # başlık → başlık
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text)  # `kod` → kod
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # *italik* → italik
    return text.strip()


#Asistanın konuşması için gerekli olan fonksiyon.
def speak(text, lang="tr", max_chunk_length=250):
    print(Fore.CYAN + f"Asistan: {text}")

    clean_text = clean_markdown(text)
    chunks = split_text_into_chunks(clean_text, max_chunk_length)

    for chunk in chunks:
        tts = gTTS(text=chunk, lang=lang)
        filename = "response.mp3" #Burada metin aslında mp3 dosyasına çeviriliyor ve asistanın okunması sağlanıyor.
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(filename)

#Benim kullanma amacım bazen varsayılan mikrofonumu kullanmadığım için mikrofonun karışması eğer bu konuda bir sorun yaşamıyorsanız düzenleyebilirsiniz.
def get_default_mic_index():
    keywords = ["wo mic", "usb", "realtek", "microphone", "mic", "input"]
    mics = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mics):
        if any(kw.lower() in name.lower() for kw in keywords):
            return index
    return 0

#Dinleme için kullandığımız fonksiyon.
def listen(mic_index, timeout=5, phrase_time_limit=None):
    r = sr.Recognizer()
    r.pause_threshold = 1.5
    r.non_speaking_duration = 1.0

    with sr.Microphone(device_index=mic_index) as source:
        r.adjust_for_ambient_noise(source)
        print(Fore.GREEN + "Dinleniyor...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            voice = r.recognize_google(audio, language="tr-TR") #Burada kullandığımız dili belirtiyoruz.
            print(Fore.YELLOW + f"Kullanıcı: {voice}")
            return voice.lower()
        except Exception as e:
            print(Fore.RED + f"Hata: {e}")
            return ""

#Hava durumu için kullandığımız fonksiyon.
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}&lang=tr&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"{city} için hava durumu: {desc}, sıcaklık {temp} derece."
        else:
            return f"{city} için hava durumu alınamadı."
    except:
        return "Hava durumu servisine erişilemiyor."


#Bu fonksiyon için ChatGPT'den destek aldım ancak muhtemelen spotify konusuna sıfırdan bir giriş yapacağım.
def parse_song_artist(text):
    # Çok basit: genelde şarkı adı başta, sanatçı sona
    # "Çilekeş Siyah" -> şarkı: Çilekeş, sanatçı: Siyah
    # Ama daha iyi ayırmak için " - " veya " tarafından " vb. aranabilir

    # Eğer " - " varsa ayır:
    if " - " in text:
        parts = text.split(" - ")
        return parts[0].strip(), parts[1].strip()
    # Yoksa boşluklarla iki parçaya ayır, son kelime sanatçı olabilir
    words = text.split()
    if len(words) >= 2:
        song = " ".join(words[:-1])
        artist = words[-1]
        return song, artist
    else:
        # Tek kelimelik ise sadece şarkı adı say
        return text, ""

#Bu fonksiyon spotify erişimi için. Muhtemelen spotify konusuna sıfırdan bir giriş yapacağım.
def play_spotify_song():
    speak("Hangi şarkıyı ve sanatçıyı çalmak istediğinizi tek seferde söyleyebilirsiniz.")
    user_input = listen(mic_index, timeout=7, phrase_time_limit=7)
    if not user_input:
        speak("Şarkı ve sanatçı adı alınamadı.")
        return

    query = user_input.strip()

    results = sp.search(q=query, type="track", limit=10)
    tracks = results.get("tracks", {}).get("items", [])

    print("Bulunan şarkılar:")
    for t in tracks:
        print(f"{t['name']} - {t['artists'][0]['name']}")

    if not tracks:
        speak("Aradığınız şarkı bulunamadı.")
        return

    devices = sp.devices()["devices"]
    if not devices:
        speak("Spotify'da aktif bir cihaz bulunamadı.")
        return

    device_id = devices[0]["id"]
    selected_track = tracks[0]
    sp.start_playback(device_id=device_id, uris=[selected_track["uri"]])

    speak(f"Spotify'da çalınıyor: {selected_track['name']} - {selected_track['artists'][0]['name']}")


#Yapay zeka modu için kullandığımız fonksiyon.
def ai_chat_loop():
        speak("Yapay zeka sohbet moduna geçildi.")
        while True:
            user_input = listen(mic_index, timeout=8, phrase_time_limit=10)
            if "çık" in user_input:
                speak("Yapay zeka modundan çıkılıyor.")
                break
            if user_input.strip() == "":
                speak("Anlayamadım, lütfen tekrar edin.")
                continue
            response = co.chat(
                message=user_input,
                temperature=0.7
            )
            speak(response.text.strip())
#Niyet algılama için kullandığımız fonksiyondur.
def detect_intent(command):
    prompt = f"""Sen bir sesli asistanın içindeki yapay zekasın. Görevin, kullanıcının niyetini anlamak.
Kullanıcıdan gelen komut: \"{command}\"
Buna karşılık olarak sadece aşağıdakilerden birini döndür:
- spotify(Şarkı veya müzik dendiğinde spotify döndür)
- kod
- hava
- saat
- youtube
- google
- not
- arama
- çık
- zeka

Sadece ve sadece bu kelimelerden biri olmalı. Hiç açıklama yapma.
"""
    response = co.chat(message=prompt, temperature=0.3)
    intent = response.text.strip().lower()
    print(f"Niyet algılandı: {intent}")
    return intent


#Aslında komutların ayarlandığı yer burası. Burada kendime ait komutlar görebilirsiniz. Siz de istediğiniz gibi detect_intent
#fonksiyonuna ekleme yapı burada ona göre bir komut ayarlayabilirsiniz.
def process_command(command):
    command = command.lower()
    intent = detect_intent(command)

    if intent == "kod": #Burası niyetleri komutlara bağladınız yer
        speak("Hangi programı kullanmak istersiniz?")
        prog_command = listen(mic_index, timeout=5, phrase_time_limit=5)
        if any(kw in prog_command for kw in ["ferece", "efar si", "frc", "ef arzi", "ef arsi", "effe", "effi", "efar", "fr"]): #İngilizce kelime algılaması zayıf olduğu için FRC (efarsi) kelimesini sürekli mikrofona söylerek aldığım çıktıları burada komut olarak ayarladım
            speak("wpilib açılıyor...")
            subprocess.Popen(['C:\\Users\\Public\\wpilib\\2025\\vscode\\Code.exe'])
        elif any(kw in prog_command for kw in ["payçarm", "pycharm", "payçal", "paytar"]):
            speak("pycharm açılıyor...")
            subprocess.Popen('C:\\Program Files\\JetBrains\\PyCharm 2025.1.1.1\\bin\\pycharm64.exe')
        elif any(kw in prog_command for kw in ["vs", "vs code", "visual studio", "vision studio"]):
            speak("visual studio açılıyor")
            subprocess.Popen('"C:\\Users\\Osma\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"')
        else:
            speak("Bu komutu anlayamadım")

    elif intent == "spotify":
        play_spotify_song()

    elif intent == "youtube":
        speak("YouTube açılıyor.")
        webbrowser.open("https://www.youtube.com")

    elif intent == "google":
        speak("Google açılıyor.")
        webbrowser.open("https://www.google.com")

    elif intent == "saat":
        now = datetime.now().strftime("%H:%M")
        speak(f"Şu an saat {now}")

    elif intent == "zeka":
        ai_chat_loop()

    elif intent == "not":
        speak("Ne not etmemi istersin?")
        note = listen(mic_index, timeout=5, phrase_time_limit=5)
        if note:
            with open("notlar.txt", "a", encoding="utf-8") as f:
                f.write(f"{note}\n")
            speak("Not kaydedildi.")

    elif intent == "arama":
        speak("Ne aramamı istersin?")
        query = listen(mic_index, timeout=5, phrase_time_limit=5)
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"{query} için arama yapılıyor.")

    elif intent == "hava":
        speak("Hangi şehir için hava durumu istersiniz?")
        city = listen(mic_index, timeout=5, phrase_time_limit=5)
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
        else:
            speak("Şehir adı anlaşılmadı.")

    elif intent == "çık":
        speak("Görüşürüz.")
        exit()

    else:
        speak("Bu komutu anlayamadım.")

def main():
    global mic_index
    mic_index = get_default_mic_index()
    speak("Google başlatıldı. 'Hey Google' dediğinde seni dinleyeceğim.")

    porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=[WAKE_WORD])
    pa = pyaudio.PyAudio()
    stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                     input=True, frames_per_buffer=porcupine.frame_length,
                     input_device_index=mic_index)

    try:
        while True:
            print(Fore.LIGHTBLACK_EX + "[Wake kelimesi bekleniyor...]")
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm_unpacked)
            if keyword_index >= 0:
                speak("Buyrun, sizi dinliyorum.")
                command = listen(mic_index, timeout=5, phrase_time_limit=7)
                if command:
                    process_command(command)
    except KeyboardInterrupt:
        print("Program durduruldu.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
