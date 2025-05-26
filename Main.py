#Maked by Airlemur
#Yardım ve destek için Osman_Rauf_Ucar (İnstagram dm)

import webbrowser
from datetime import datetime
from colorama import Fore, init
import pvporcupine
import pyaudio
import struct
import Constants
from function import ListenWriteAndSpeak, ProcessCommand

init(autoreset=True)
mic_index = 0

def main():
    mic_index = ListenWriteAndSpeak.get_default_mic_index()
    ListenWriteAndSpeak.speak("Google başlatıldı. 'Hey Google' dediğinde seni dinleyeceğim.")

    porcupine = pvporcupine.create(access_key=Constants.PORCUPINE_ACCESS_KEY, keywords=[Constants.WAKE_WORD])
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
                ListenWriteAndSpeak.speak("Buyrun, sizi dinliyorum.")
                command = ListenWriteAndSpeak.listen(mic_index, timeout=5, phrase_time_limit=7)
                if command:
                    ProcessCommand.process_command(command)
    except KeyboardInterrupt:
        print("Program durduruldu.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
