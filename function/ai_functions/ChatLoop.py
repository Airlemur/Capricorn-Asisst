#Yapay zeka modu için kullandığımız fonksiyon.
import Main
from function import ListenWriteAndSpeak
import Constants


def ai_chat_loop():
        ListenWriteAndSpeak.speak("Yapay zeka sohbet moduna geçildi.")
        while True:
            user_input = ListenWriteAndSpeak.listen(Main.mic_index, timeout=8, phrase_time_limit=10)
            if "çık" in user_input:
                ListenWriteAndSpeak.speak("Yapay zeka modundan çıkılıyor.")
                break
            if user_input.strip() == "":
                ListenWriteAndSpeak.speak("Anlayamadım, lütfen tekrar edin.")
                continue
            response = Constants.co.chat(
                message=user_input,
                temperature=0.7
            )
            ListenWriteAndSpeak.speak(response.text.strip())
