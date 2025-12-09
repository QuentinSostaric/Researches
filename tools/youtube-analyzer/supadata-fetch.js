import { Supadata } from "@supadata/js";
import fs from "fs/promises";

const API_KEY = "sd_c6d07c43a85f83c938383a2ff08a41cb";
const CHANNEL_URL = "https://www.youtube.com/@TheMasculineHome";
const OUTPUT_DIR = "/home/user/Researches/researches/masculine-home-products";

const supadata = new Supadata({ apiKey: API_KEY });

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  console.log("=" .repeat(80));
  console.log("🔍 Analyse de la chaîne:", CHANNEL_URL);
  console.log("=".repeat(80));

  // Étape 1: Récupérer la liste des vidéos
  console.log("\n📺 Récupération de la liste des vidéos...");

  const channelVideos = await supadata.youtube.channel.videos({
    id: CHANNEL_URL,
    type: "video", // On prend uniquement les vidéos (pas les shorts)
    limit: 100,
  });

  console.log(`✅ Vidéos trouvées: ${channelVideos.videoIds.length}`);

  // Sauvegarder la liste des vidéos
  await fs.writeFile(
    `${OUTPUT_DIR}/video-list.json`,
    JSON.stringify(channelVideos, null, 2)
  );
  console.log(`💾 Liste sauvegardée: ${OUTPUT_DIR}/video-list.json`);

  // Étape 2: Récupérer les métadonnées de chaque vidéo
  console.log("\n📋 Récupération des métadonnées des vidéos...");

  const videosMetadata = [];
  for (let i = 0; i < channelVideos.videoIds.length; i++) {
    const videoId = channelVideos.videoIds[i];
    console.log(`[${i + 1}/${channelVideos.videoIds.length}] ${videoId}`);

    try {
      const video = await supadata.youtube.video({ id: videoId });
      videosMetadata.push({
        id: videoId,
        title: video.title,
        description: video.description,
        duration: video.duration,
        publishedAt: video.publishedAt,
        url: `https://www.youtube.com/watch?v=${videoId}`,
      });
      console.log(`  ✅ ${video.title?.substring(0, 50)}...`);
    } catch (error) {
      console.log(`  ⚠️ Erreur: ${error.message}`);
      videosMetadata.push({ id: videoId, error: error.message });
    }

    await sleep(300); // Pause pour éviter le rate limiting
  }

  await fs.writeFile(
    `${OUTPUT_DIR}/videos-metadata.json`,
    JSON.stringify(videosMetadata, null, 2)
  );
  console.log(`💾 Métadonnées sauvegardées: ${OUTPUT_DIR}/videos-metadata.json`);

  // Étape 3: Récupérer les transcriptions
  console.log("\n📝 Récupération des transcriptions...");

  const transcripts = [];
  for (let i = 0; i < channelVideos.videoIds.length; i++) {
    const videoId = channelVideos.videoIds[i];
    const metadata = videosMetadata.find((v) => v.id === videoId);
    console.log(
      `[${i + 1}/${channelVideos.videoIds.length}] ${metadata?.title?.substring(0, 50) || videoId}...`
    );

    try {
      const transcript = await supadata.youtube.transcript({
        url: `https://www.youtube.com/watch?v=${videoId}`,
      });

      transcripts.push({
        id: videoId,
        title: metadata?.title,
        url: `https://www.youtube.com/watch?v=${videoId}`,
        language: transcript.lang,
        content: transcript.content,
        fullText: transcript.content?.map((c) => c.text).join(" "),
      });

      console.log(
        `  ✅ Transcription récupérée (${transcript.content?.length || 0} segments)`
      );
    } catch (error) {
      console.log(`  ⚠️ Pas de transcription: ${error.message}`);
      transcripts.push({
        id: videoId,
        title: metadata?.title,
        url: `https://www.youtube.com/watch?v=${videoId}`,
        error: error.message,
      });
    }

    await sleep(500); // Pause pour éviter le rate limiting
  }

  // Sauvegarder les transcriptions
  await fs.writeFile(
    `${OUTPUT_DIR}/transcripts.json`,
    JSON.stringify(transcripts, null, 2)
  );

  console.log("\n" + "=".repeat(80));
  console.log("✅ Analyse terminée!");
  console.log(`💾 Transcriptions sauvegardées: ${OUTPUT_DIR}/transcripts.json`);

  // Statistiques
  const withTranscript = transcripts.filter((t) => t.content).length;
  console.log("\n📊 Statistiques:");
  console.log(`   - Vidéos analysées: ${transcripts.length}`);
  console.log(`   - Avec transcription: ${withTranscript}`);
  console.log(`   - Sans transcription: ${transcripts.length - withTranscript}`);
}

main().catch(console.error);
