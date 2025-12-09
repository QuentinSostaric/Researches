import ytpl from 'ytpl';

async function listChannelVideos(channelUrl) {
  try {
    console.log(`Récupération des vidéos de: ${channelUrl}\n`);

    // Récupérer les informations de la playlist/chaîne
    const playlist = await ytpl(channelUrl, { limit: Infinity });

    console.log(`Chaîne: ${playlist.title}`);
    console.log(`Nombre de vidéos: ${playlist.items.length}\n`);
    console.log('='.repeat(80));

    const videos = playlist.items.map((item, index) => ({
      index: index + 1,
      title: item.title,
      id: item.id,
      url: item.shortUrl,
      duration: item.duration,
      durationSec: item.durationSec
    }));

    // Afficher la liste
    videos.forEach(video => {
      console.log(`\n${video.index}. ${video.title}`);
      console.log(`   ID: ${video.id}`);
      console.log(`   URL: ${video.url}`);
      console.log(`   Durée: ${video.duration}`);
    });

    // Exporter en JSON
    console.log('\n' + '='.repeat(80));
    console.log('\nJSON Export:');
    console.log(JSON.stringify(videos, null, 2));

    return videos;
  } catch (error) {
    console.error('Erreur:', error.message);
    process.exit(1);
  }
}

// Récupérer l'URL depuis les arguments
const channelUrl = process.argv[2] || 'https://www.youtube.com/@TheMasculineHome';
listChannelVideos(channelUrl);
