import { fetch } from 'undici';

async function resolveChannelHandle(handleUrl) {
  try {
    console.log(`Résolution du handle: ${handleUrl}`);

    // Récupérer la page de la chaîne
    const response = await fetch(handleUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
      }
    });

    const html = await response.text();

    // Chercher le channel ID dans différents patterns
    const patterns = [
      /"channelId":"(UC[a-zA-Z0-9_-]{22})"/,
      /channel_id=([a-zA-Z0-9_-]+)/,
      /"externalId":"(UC[a-zA-Z0-9_-]{22})"/,
      /\/channel\/(UC[a-zA-Z0-9_-]{22})/
    ];

    for (const pattern of patterns) {
      const match = html.match(pattern);
      if (match && match[1]) {
        console.log(`Channel ID trouvé: ${match[1]}`);
        return match[1];
      }
    }

    // Chercher l'URL canonique
    const canonicalMatch = html.match(/<link rel="canonical" href="([^"]+)"/);
    if (canonicalMatch) {
      console.log(`URL canonique: ${canonicalMatch[1]}`);
      const channelIdMatch = canonicalMatch[1].match(/channel\/(UC[a-zA-Z0-9_-]{22})/);
      if (channelIdMatch) {
        return channelIdMatch[1];
      }
    }

    console.log('Channel ID non trouvé dans la page');
    return null;
  } catch (error) {
    console.error('Erreur:', error.message);
    return null;
  }
}

// Test
const handleUrl = process.argv[2] || 'https://www.youtube.com/@TheMasculineHome';
resolveChannelHandle(handleUrl).then(id => {
  if (id) {
    console.log(`\nURL de la chaîne: https://www.youtube.com/channel/${id}`);
    console.log(`URL des vidéos: https://www.youtube.com/channel/${id}/videos`);
  }
});
