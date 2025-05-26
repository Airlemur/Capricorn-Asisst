#Aslında komutların ayarlandığı yer burası. Burada kendime ait komutlar görebilirsiniz. Siz de istediğiniz gibi detect_intent
#fonksiyonuna ekleme yapı burada ona göre bir komut ayarlayabilirsiniz.
import datetime
import webbrowser

import Main
from function import ListenWriteAndSpeak, Spotify, Weather
from function.ai_functions import DetecetIntent, ChatLoop
import subprocess


def process_command(command):
    command = command.lower()
    intent = DetecetIntent.detect_intent(command)

    if intent == "kod": #Burası niyetleri komutlara bağladınız yer
        ListenWriteAndSpeak.speak("Hangi programı kullanmak istersiniz?")
        prog_command = ListenWriteAndSpeak.listen(Main.mic_index, timeout=5, phrase_time_limit=5)
        if any(kw in prog_command for kw in ["ferece", "efar si", "frc", "ef arzi", "ef arsi", "effe", "effi", "efar", "fr"]): #İngilizce kelime algılaması zayıf olduğu için FRC (efarsi) kelimesini sürekli mikrofona söylerek aldığım çıktıları burada komut olarak ayarladım
            ListenWriteAndSpeak.speak("wpilib açılıyor...")
            subprocess.Popen(['C:\\Users\\Public\\wpilib\\2025\\vscode\\Code.exe'])
        elif any(kw in prog_command for kw in ["payçarm", "pycharm", "payçal", "paytar"]):
            ListenWriteAndSpeak.speak("pycharm açılıyor...")
            subprocess.Popen('C:\\Program Files\\JetBrains\\PyCharm 2025.1.1.1\\bin\\pycharm64.exe')
        elif any(kw in prog_command for kw in ["vs", "vs code", "visual studio", "vision studio"]):
            ListenWriteAndSpeak.speak("visual studio açılıyor")
            subprocess.Popen('"C:\\Users\\Osma\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"')
        else:
            ListenWriteAndSpeak.speak("Bu komutu anlayamadım")

    elif intent == "spotify":
        Spotify.play_spotify_song()

    elif intent == "youtube":
        ListenWriteAndSpeak.speak("YouTube açılıyor.")
        webbrowser.open("https://www.youtube.com")

    elif intent == "google":
        ListenWriteAndSpeak.speak("Google açılıyor.")
        webbrowser.open("https://www.google.com")

    elif intent == "saat":
        now = datetime.now().strftime("%H:%M")
        ListenWriteAndSpeak.speak(f"Şu an saat {now}")

    elif intent == "zeka":
        ChatLoop.ai_chat_loop()

    elif intent == "not":
        ListenWriteAndSpeak.speak("Ne not etmemi istersin?")
        note = ListenWriteAndSpeak.listen(Main.mic_index, timeout=5, phrase_time_limit=5)
        if note:
            with open("notlar.txt", "a", encoding="utf-8") as f:
                f.write(f"{note}\n")
            ListenWriteAndSpeak.speak("Not kaydedildi.")

    elif intent == "arama":
        ListenWriteAndSpeak.speak("Ne aramamı istersin?")
        query = ListenWriteAndSpeak.listen(Main.mic_index, timeout=5, phrase_time_limit=5)
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            ListenWriteAndSpeak.speak(f"{query} için arama yapılıyor.")

    elif intent == "hava":
        ListenWriteAndSpeak.speak("Hangi şehir için hava durumu istersiniz?")
        city = ListenWriteAndSpeak.listen(Main.mic_index, timeout=5, phrase_time_limit=5)
        if city:
            weather_info = Weather.get_weather(city)
            ListenWriteAndSpeak.speak(weather_info)
        else:
            ListenWriteAndSpeak.speak("Şehir adı anlaşılmadı.")

    elif intent == "yapımcı":
        ListenWriteAndSpeak.speak("Benim ilk yapımcım Airlemur'dur ancak açık kaynaklı bir proje olduğum için herkes tarafından geliştiriliyorum.")

    elif intent == "küfür":
        ListenWriteAndSpeak.speak("Bu konuşmayı sonlandırıyorum")
        exit()

    elif intent == "cinsellik":
        ListenWriteAndSpeak.speak("Maalesef cinsellik hakkında konuşmuyorum")
        exit()

    elif intent == "çık":
        ListenWriteAndSpeak.speak("Görüşürüz.")
        exit()

    else:
        ListenWriteAndSpeak.speak("Bu komutu anlayamadım.")