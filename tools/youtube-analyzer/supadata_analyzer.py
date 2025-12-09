#!/usr/bin/env python3
"""
Script pour récupérer les vidéos et transcriptions d'une chaîne YouTube
via l'API Supadata.ai
"""

import json
import sys
import time
import urllib.request
import urllib.error
import ssl

# Configuration
API_KEY = "sd_c6d07c43a85f83c938383a2ff08a41cb"
BASE_URL = "https://api.supadata.ai/v1"

# Désactiver la vérification SSL (pour contourner le proxy)
ssl._create_default_https_context = ssl._create_unverified_context

def api_request(endpoint, params=None):
    """Effectue une requête à l'API Supadata"""
    url = f"{BASE_URL}{endpoint}"

    if params:
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        url = f"{url}?{query_string}"

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Erreur HTTP {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Détails: {error_body}")
        except:
            pass
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def get_channel_videos(channel_url, video_type="all", limit=100):
    """Récupère la liste des vidéos d'une chaîne"""
    print(f"\n📺 Récupération des vidéos de: {channel_url}")

    result = api_request("/youtube/channel/videos", {
        "id": channel_url,
        "type": video_type,
        "limit": limit
    })

    if result:
        video_ids = result.get("videoIds", [])
        short_ids = result.get("shortIds", [])
        live_ids = result.get("liveIds", [])

        print(f"✅ Vidéos trouvées: {len(video_ids)}")
        print(f"✅ Shorts trouvés: {len(short_ids)}")
        print(f"✅ Lives trouvés: {len(live_ids)}")

        return {
            "videos": video_ids,
            "shorts": short_ids,
            "lives": live_ids
        }

    return None

def get_video_transcript(video_id, lang="en"):
    """Récupère la transcription d'une vidéo"""
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    result = api_request("/youtube/transcript", {
        "url": video_url,
        "lang": lang
    })

    if result:
        return result

    # Essayer sans spécifier la langue
    result = api_request("/youtube/transcript", {
        "url": video_url
    })

    return result

def get_video_metadata(video_id):
    """Récupère les métadonnées d'une vidéo"""
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    result = api_request("/youtube/video", {
        "url": video_url
    })

    return result

def format_timecode(ms):
    """Convertit des millisecondes en timecode MM:SS"""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def analyze_channel(channel_url, output_dir="."):
    """Analyse complète d'une chaîne YouTube"""
    print("=" * 80)
    print(f"🔍 Analyse de la chaîne: {channel_url}")
    print("=" * 80)

    # Étape 1: Récupérer la liste des vidéos
    videos_data = get_channel_videos(channel_url, limit=200)

    if not videos_data:
        print("❌ Impossible de récupérer les vidéos")
        return None

    all_video_ids = videos_data["videos"] + videos_data["shorts"]

    # Sauvegarder la liste des vidéos
    videos_file = f"{output_dir}/video-list.json"
    with open(videos_file, 'w', encoding='utf-8') as f:
        json.dump(videos_data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Liste des vidéos sauvegardée: {videos_file}")

    # Étape 2: Récupérer les métadonnées et transcriptions
    results = {
        "channel_url": channel_url,
        "total_videos": len(all_video_ids),
        "videos": []
    }

    print(f"\n📝 Récupération des transcriptions ({len(all_video_ids)} vidéos)...")

    for i, video_id in enumerate(all_video_ids):
        print(f"\n[{i+1}/{len(all_video_ids)}] Vidéo: {video_id}")

        video_data = {
            "id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "title": None,
            "transcript": None,
            "full_text": None
        }

        # Récupérer les métadonnées
        metadata = get_video_metadata(video_id)
        if metadata:
            video_data["title"] = metadata.get("title", "Sans titre")
            video_data["duration"] = metadata.get("duration")
            video_data["description"] = metadata.get("description")
            print(f"  📌 Titre: {video_data['title'][:60]}...")

        # Récupérer la transcription
        transcript = get_video_transcript(video_id)
        if transcript and "content" in transcript:
            video_data["transcript"] = transcript["content"]
            video_data["language"] = transcript.get("lang", "unknown")

            # Créer le texte complet
            full_text = " ".join([item.get("text", "") for item in transcript["content"]])
            video_data["full_text"] = full_text

            print(f"  ✅ Transcription récupérée ({len(transcript['content'])} segments)")
        else:
            print(f"  ⚠️ Pas de transcription disponible")

        results["videos"].append(video_data)

        # Pause pour éviter le rate limiting
        time.sleep(0.5)

    # Sauvegarder les résultats
    transcripts_file = f"{output_dir}/transcripts.json"
    with open(transcripts_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 80}")
    print(f"✅ Analyse terminée!")
    print(f"💾 Transcriptions sauvegardées: {transcripts_file}")

    # Statistiques
    with_transcript = sum(1 for v in results["videos"] if v["transcript"])
    print(f"\n📊 Statistiques:")
    print(f"   - Vidéos analysées: {len(results['videos'])}")
    print(f"   - Avec transcription: {with_transcript}")
    print(f"   - Sans transcription: {len(results['videos']) - with_transcript}")

    return results

if __name__ == "__main__":
    import urllib.parse

    if len(sys.argv) < 2:
        print("Usage: python supadata_analyzer.py <channel_url> [output_dir]")
        print()
        print("Exemple:")
        print("  python supadata_analyzer.py https://www.youtube.com/@TheMasculineHome ./output")
        sys.exit(1)

    channel_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    analyze_channel(channel_url, output_dir)
