#!/usr/bin/env python3
"""
Script pour récupérer les transcriptions via l'API Supadata.ai
Utilise la liste de vidéos déjà récupérée
"""

import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl

# Configuration
API_KEY = "sd_c6d07c43a85f83c938383a2ff08a41cb"
BASE_URL = "https://api.supadata.ai/v1"
OUTPUT_DIR = "/home/user/Researches/researches/masculine-home-products"

# Désactiver la vérification SSL
ssl._create_default_https_context = ssl._create_unverified_context

def api_request(endpoint, params=None, retries=3, delay=2):
    """Effectue une requête à l'API Supadata avec retries"""
    url = f"{BASE_URL}{endpoint}"

    if params:
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        url = f"{url}?{query_string}"

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit
                wait_time = delay * (2 ** attempt)
                print(f"    ⏳ Rate limit - attente {wait_time}s...")
                time.sleep(wait_time)
                continue
            elif e.code == 503:  # Service unavailable
                wait_time = delay * (2 ** attempt)
                print(f"    ⏳ Service indisponible - attente {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            return None

    return None

def get_video_metadata(video_id):
    """Récupère les métadonnées d'une vidéo"""
    return api_request("/youtube/video", {"id": video_id})

def get_transcript(video_id):
    """Récupère la transcription d'une vidéo"""
    return api_request("/youtube/transcript", {
        "url": f"https://www.youtube.com/watch?v={video_id}"
    })

def main():
    print("=" * 80)
    print("📝 Récupération des transcriptions - The Masculine Home")
    print("=" * 80)

    # Charger la liste des vidéos
    with open(f"{OUTPUT_DIR}/video-list.json", 'r') as f:
        video_data = json.load(f)

    video_ids = video_data.get("videos", [])
    print(f"\n📺 {len(video_ids)} vidéos à traiter")

    results = []

    for i, video_id in enumerate(video_ids):
        print(f"\n[{i+1}/{len(video_ids)}] Vidéo: {video_id}")

        video_info = {
            "id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "title": None,
            "transcript": None,
            "fullText": None
        }

        # Récupérer les métadonnées
        metadata = get_video_metadata(video_id)
        if metadata:
            video_info["title"] = metadata.get("title", "Sans titre")
            video_info["description"] = metadata.get("description")
            video_info["duration"] = metadata.get("duration")
            print(f"  📌 {video_info['title'][:60]}...")
        else:
            print(f"  ⚠️ Métadonnées non disponibles")

        # Pause pour éviter le rate limiting
        time.sleep(1)

        # Récupérer la transcription
        transcript = get_transcript(video_id)
        if transcript and "content" in transcript:
            video_info["transcript"] = transcript["content"]
            video_info["language"] = transcript.get("lang", "unknown")
            video_info["fullText"] = " ".join([c.get("text", "") for c in transcript["content"]])
            print(f"  ✅ Transcription: {len(transcript['content'])} segments")
        else:
            print(f"  ⚠️ Pas de transcription")

        results.append(video_info)

        # Pause entre chaque vidéo
        time.sleep(1.5)

        # Sauvegarder périodiquement (toutes les 10 vidéos)
        if (i + 1) % 10 == 0:
            with open(f"{OUTPUT_DIR}/transcripts.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  💾 Sauvegarde intermédiaire ({i+1} vidéos)")

    # Sauvegarder les résultats finaux
    with open(f"{OUTPUT_DIR}/transcripts.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("✅ Terminé!")

    # Statistiques
    with_transcript = sum(1 for v in results if v.get("transcript"))
    print(f"\n📊 Statistiques:")
    print(f"   - Vidéos traitées: {len(results)}")
    print(f"   - Avec transcription: {with_transcript}")
    print(f"   - Sans transcription: {len(results) - with_transcript}")

if __name__ == "__main__":
    main()
