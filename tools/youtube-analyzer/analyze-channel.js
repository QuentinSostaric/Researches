import ytpl from '@distube/ytpl';
import { YoutubeTranscript } from 'youtube-transcript';
import fs from 'fs/promises';

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getTranscript(videoId) {
  try {
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    if (!transcript || transcript.length === 0) {
      return null;
    }

    return transcript.map(item => {
      const minutes = Math.floor(item.offset / 60000);
      const seconds = Math.floor((item.offset % 60000) / 1000);
      const timecode = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return {
        timecode,
        offsetMs: item.offset,
        text: item.text
      };
    });
  } catch (error) {
    console.error(`  Erreur transcription: ${error.message}`);
    return null;
  }
}

async function analyzeChannel(channelUrl, outputFile) {
  try {
    console.log(`\n🔍 Analyse de la chaîne: ${channelUrl}\n`);
    console.log('='.repeat(80));

    // Récupérer la liste des vidéos
    console.log('\n📺 Récupération de la liste des vidéos...');
    const playlist = await ytpl(channelUrl, { limit: Infinity });

    console.log(`✅ Chaîne: ${playlist.title}`);
    console.log(`✅ Nombre de vidéos trouvées: ${playlist.items.length}\n`);

    const results = {
      channel: {
        title: playlist.title,
        url: channelUrl,
        videoCount: playlist.items.length
      },
      videos: []
    };

    // Analyser chaque vidéo
    for (let i = 0; i < playlist.items.length; i++) {
      const video = playlist.items[i];
      console.log(`\n[${i + 1}/${playlist.items.length}] ${video.title}`);
      console.log(`  URL: ${video.shortUrl}`);

      const videoData = {
        index: i + 1,
        title: video.title,
        id: video.id,
        url: video.shortUrl,
        duration: video.duration,
        transcript: null,
        fullText: null
      };

      // Récupérer la transcription
      console.log('  📝 Récupération de la transcription...');
      const transcript = await getTranscript(video.id);

      if (transcript) {
        videoData.transcript = transcript;
        videoData.fullText = transcript.map(t => t.text).join(' ');
        console.log(`  ✅ Transcription récupérée (${transcript.length} segments)`);
      } else {
        console.log('  ⚠️ Pas de transcription disponible');
      }

      results.videos.push(videoData);

      // Pause pour éviter le rate limiting
      if (i < playlist.items.length - 1) {
        await sleep(1000);
      }
    }

    // Sauvegarder les résultats
    const output = outputFile || 'channel-analysis.json';
    await fs.writeFile(output, JSON.stringify(results, null, 2), 'utf-8');
    console.log(`\n${'='.repeat(80)}`);
    console.log(`\n✅ Analyse terminée! Résultats sauvegardés dans: ${output}`);

    // Statistiques
    const withTranscript = results.videos.filter(v => v.transcript).length;
    console.log(`\n📊 Statistiques:`);
    console.log(`   - Vidéos analysées: ${results.videos.length}`);
    console.log(`   - Avec transcription: ${withTranscript}`);
    console.log(`   - Sans transcription: ${results.videos.length - withTranscript}`);

    return results;
  } catch (error) {
    console.error('Erreur:', error.message);
    process.exit(1);
  }
}

// Arguments
const channelUrl = process.argv[2] || 'https://www.youtube.com/@TheMasculineHome';
const outputFile = process.argv[3] || 'channel-analysis.json';

analyzeChannel(channelUrl, outputFile);
