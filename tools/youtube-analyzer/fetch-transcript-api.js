// Script pour récupérer les transcriptions via l'API YouTube Subtitles
// en contournant les restrictions du proxy

import https from 'https';
import http from 'http';

const agent = new https.Agent({
  rejectUnauthorized: false
});

async function fetchWithRetry(url, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, {
        ...options,
        agent
      });
      return response;
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}

// Fonction pour extraire les sous-titres depuis le XML de YouTube
async function getYouTubeSubtitles(videoId) {
  try {
    // URL directe pour les sous-titres auto-générés
    const subtitleUrl = `https://www.youtube.com/api/timedtext?v=${videoId}&lang=en&fmt=srv3`;

    console.log(`Tentative de récupération des sous-titres pour: ${videoId}`);
    console.log(`URL: ${subtitleUrl}`);

    const response = await fetchWithRetry(subtitleUrl);

    if (!response.ok) {
      console.log(`Status: ${response.status}`);
      return null;
    }

    const text = await response.text();
    console.log('Réponse reçue:', text.substring(0, 500));

    return text;
  } catch (error) {
    console.error('Erreur:', error.message);
    return null;
  }
}

// Test avec un ID vidéo
const videoId = process.argv[2] || 'test';
getYouTubeSubtitles(videoId);
