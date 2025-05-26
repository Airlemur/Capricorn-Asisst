from spotipy import SpotifyOAuth
import Main
import spotipy
import Constants
import spotipy
import speech_recognition as sr

from function import ListenWriteAndSpeak

scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=Constants.SPOTIPY_CLIENT_ID,
    client_secret=Constants.SPOTIPY_CLIENT_SECRET,
    redirect_uri=Constants.SPOTIPY_REDIRECT_URI,
    scope=scope
))

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
    ListenWriteAndSpeak.speak("Hangi şarkıyı ve sanatçıyı çalmak istediğinizi tek seferde söyleyebilirsiniz.")
    user_input = ListenWriteAndSpeak.listen( Main.mic_index, timeout=7, phrase_time_limit=7)
    if not user_input:
        ListenWriteAndSpeak.speak("Şarkı ve sanatçı adı alınamadı.")
        return

    query = user_input.strip()

    results = sp.search(q=query, type="track", limit=10)
    tracks = results.get("tracks", {}).get("items", [])

    print("Bulunan şarkılar:")
    for t in tracks:
        print(f"{t['name']} - {t['artists'][0]['name']}")

    if not tracks:
        ListenWriteAndSpeak.speak("Aradığınız şarkı bulunamadı.")
        return

    devices =  sp.devices()["devices"]
    if not devices:
        ListenWriteAndSpeak.speak("Spotify'da aktif bir cihaz bulunamadı.")
        return

    device_id = devices[0]["id"]
    selected_track = tracks[0]
    sp.start_playback(device_id=device_id, uris=[selected_track["uri"]])

    ListenWriteAndSpeak.speak(f"Spotify'da çalınıyor: {selected_track['name']} - {selected_track['artists'][0]['name']}")