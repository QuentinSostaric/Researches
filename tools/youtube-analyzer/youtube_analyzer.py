#!/usr/bin/env python3
"""
YouTube Channel Analyzer - Récupère les vidéos et transcriptions d'une chaîne YouTube
"""

import json
import sys
import os
import re
import ssl
import urllib.request
from urllib.parse import quote
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Désactiver la vérification SSL pour contourner le proxy
ssl._create_default_https_context = ssl._create_unverified_context

def get_channel_videos(channel_url):
    """Récupère la liste des vidéos d'une chaîne YouTube via scraping"""
    try:
        # Extraire le handle ou channel ID
        if '@' in channel_url:
            channel_url = channel_url.rstrip('/') + '/videos'

        print(f"Récupération des vidéos depuis: {channel_url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

        req = urllib.request.Request(channel_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')

        # Extraire les IDs et titres des vidéos depuis le HTML
        videos = []

        # Pattern pour trouver les vidéos dans le JSON initial
        pattern = r'"videoId":"([a-zA-Z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"([^"]+)"\}'
        matches = re.findall(pattern, html)

        # Dédupliquer
        seen_ids = set()
        for video_id, title in matches:
            if video_id not in seen_ids:
                seen_ids.add(video_id)
                videos.append({
                    'id': video_id,
                    'title': title,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })

        # Si pas trouvé avec le premier pattern, essayer un autre
        if not videos:
            pattern2 = r'"videoId":"([a-zA-Z0-9_-]{11})"'
            video_ids = list(set(re.findall(pattern2, html)))

            # Chercher les titres séparément
            title_pattern = r'"title":\s*\{\s*"runs":\s*\[\s*\{\s*"text":\s*"([^"]+)"'
            titles = re.findall(title_pattern, html)

            for i, video_id in enumerate(video_ids[:50]):  # Limiter à 50 vidéos
                title = titles[i] if i < len(titles) else f"Video {i+1}"
                videos.append({
                    'id': video_id,
                    'title': title,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })

        print(f"Trouvé {len(videos)} vidéos")
        return videos

    except Exception as e:
        print(f"Erreur lors de la récupération des vidéos: {e}")
        return []

def get_video_transcript(video_id, languages=['en', 'en-US', 'en-GB', 'fr']):
    """Récupère la transcription d'une vidéo"""
    try:
        # Essayer d'obtenir la transcription dans différentes langues
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Chercher une transcription manuelle d'abord
        transcript = None
        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except:
            try:
                # Sinon, prendre la transcription auto-générée
                transcript = transcript_list.find_generated_transcript(languages)
            except:
                # Prendre n'importe quelle transcription disponible
                for t in transcript_list:
                    transcript = t
                    break

        if transcript:
            data = transcript.fetch()
            return [{
                'text': item['text'],
                'start': item['start'],
                'duration': item.get('duration', 0),
                'timecode': format_timecode(item['start'])
            } for item in data]

        return None

    except TranscriptsDisabled:
        print(f"  Transcriptions désactivées pour {video_id}")
        return None
    except NoTranscriptFound:
        print(f"  Pas de transcription trouvée pour {video_id}")
        return None
    except Exception as e:
        print(f"  Erreur transcription: {e}")
        return None

def format_timecode(seconds):
    """Convertit des secondes en timecode MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def analyze_channel(channel_url, output_file='channel_analysis.json'):
    """Analyse complète d'une chaîne YouTube"""
    print(f"\n{'='*80}")
    print(f"Analyse de la chaîne: {channel_url}")
    print(f"{'='*80}\n")

    # Récupérer la liste des vidéos
    videos = get_channel_videos(channel_url)

    if not videos:
        print("Aucune vidéo trouvée!")
        return None

    results = {
        'channel_url': channel_url,
        'video_count': len(videos),
        'videos': []
    }

    # Analyser chaque vidéo
    for i, video in enumerate(videos):
        print(f"\n[{i+1}/{len(videos)}] {video['title'][:60]}...")

        video_data = {
            'index': i + 1,
            'id': video['id'],
            'title': video['title'],
            'url': video['url'],
            'transcript': None,
            'full_text': None
        }

        # Récupérer la transcription
        transcript = get_video_transcript(video['id'])

        if transcript:
            video_data['transcript'] = transcript
            video_data['full_text'] = ' '.join([t['text'] for t in transcript])
            print(f"  ✓ Transcription récupérée ({len(transcript)} segments)")
        else:
            print(f"  ✗ Pas de transcription")

        results['videos'].append(video_data)

    # Sauvegarder les résultats
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*80}")
    print(f"Analyse terminée! Résultats sauvegardés dans: {output_file}")

    # Statistiques
    with_transcript = sum(1 for v in results['videos'] if v['transcript'])
    print(f"\nStatistiques:")
    print(f"  - Vidéos analysées: {len(results['videos'])}")
    print(f"  - Avec transcription: {with_transcript}")
    print(f"  - Sans transcription: {len(results['videos']) - with_transcript}")

    return results

def get_single_transcript(video_id):
    """Récupère uniquement la transcription d'une vidéo"""
    print(f"Récupération de la transcription pour: {video_id}")

    transcript = get_video_transcript(video_id)

    if transcript:
        print(f"\nTranscription ({len(transcript)} segments):\n")
        for t in transcript:
            print(f"[{t['timecode']}] {t['text']}")

        print(f"\n{'='*80}")
        print("\nTexte complet:")
        print(' '.join([t['text'] for t in transcript]))
    else:
        print("Pas de transcription disponible")

    return transcript

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python youtube_analyzer.py <channel_url> [output_file]")
        print("  python youtube_analyzer.py --video <video_id>")
        print()
        print("Exemples:")
        print("  python youtube_analyzer.py https://www.youtube.com/@TheMasculineHome")
        print("  python youtube_analyzer.py --video dQw4w9WgXcQ")
        sys.exit(1)

    if sys.argv[1] == '--video' and len(sys.argv) >= 3:
        get_single_transcript(sys.argv[2])
    else:
        channel_url = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'channel_analysis.json'
        analyze_channel(channel_url, output_file)
