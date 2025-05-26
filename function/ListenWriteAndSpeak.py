import re
import time
import speech_recognition as sr
from colorama import Fore
from gtts import gTTS
import os
import pygame

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
