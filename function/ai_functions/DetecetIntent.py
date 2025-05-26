import Constants

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
- küfür (Kullanıcının küfür etmesi durumunda küfür döndür)
- yapımcı (Bu asistanın yapımcısı hakkında soru sorulursa bunu döndür)
- cinsellik (Eğer kullanıcının söylemi cinsellik öğeleri içeriyorsa bunu döndür ama unutma küfürleri bu kategoriye sokma)

Sadece ve sadece bu kelimelerden biri olmalı. Hiç açıklama yapma.
"""
    response = Constants.co.chat(message=prompt, temperature=0.3)
    intent = response.text.strip().lower()
    print(f"Niyet algılandı: {intent}")
    return intent