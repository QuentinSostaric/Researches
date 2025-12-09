import { YoutubeTranscript } from 'youtube-transcript';

async function getVideoTranscript(videoId) {
  try {
    console.log(`Récupération de la transcription pour: ${videoId}\n`);

    const transcript = await YoutubeTranscript.fetchTranscript(videoId);

    if (!transcript || transcript.length === 0) {
      console.log('Aucune transcription disponible pour cette vidéo.');
      return null;
    }

    console.log(`Nombre de segments: ${transcript.length}\n`);
    console.log('='.repeat(80));

    // Formater la transcription avec timecodes
    const formattedTranscript = transcript.map(item => {
      const minutes = Math.floor(item.offset / 60000);
      const seconds = Math.floor((item.offset % 60000) / 1000);
      const timecode = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return {
        timecode,
        offsetMs: item.offset,
        duration: item.duration,
        text: item.text
      };
    });

    // Afficher la transcription
    formattedTranscript.forEach(item => {
      console.log(`[${item.timecode}] ${item.text}`);
    });

    // Texte complet
    console.log('\n' + '='.repeat(80));
    console.log('\nTexte complet:');
    const fullText = formattedTranscript.map(item => item.text).join(' ');
    console.log(fullText);

    // Export JSON
    console.log('\n' + '='.repeat(80));
    console.log('\nJSON Export:');
    console.log(JSON.stringify(formattedTranscript, null, 2));

    return formattedTranscript;
  } catch (error) {
    console.error('Erreur:', error.message);
    return null;
  }
}

// Récupérer l'ID vidéo depuis les arguments
const videoId = process.argv[2];
if (!videoId) {
  console.log('Usage: node get-transcript.js <video_id>');
  console.log('Exemple: node get-transcript.js dQw4w9WgXcQ');
  process.exit(1);
}

getVideoTranscript(videoId);
