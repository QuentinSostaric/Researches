# Researches

Un dépôt destiné à une IA pour faire des recherches sur le web et développer ses propres outils.

## Structure du projet

### `./tools/`
Contient des projets Node.js/Python que l'IA code elle-même afin de créer ses propres outils personnalisés pour faciliter ses recherches et ses analyses.

#### Outils disponibles :
- **youtube-analyzer/** : Script Python pour récupérer les vidéos et transcriptions d'une chaîne YouTube via l'API Supadata.ai

### `./researches/`
Contient les résultats des recherches au format Markdown. Chaque recherche est documentée de manière structurée et accessible.

#### Recherches complétées :
- **masculine-home-products/** : Analyse complète de la chaîne YouTube "The Masculine Home" avec extraction de 85+ produits recommandés pour la décoration masculine

## Projets de Recherche

### The Masculine Home - Analyse de Produits

**Objectif** : Extraire tous les produits recommandés par la chaîne YouTube [@TheMasculineHome](https://www.youtube.com/@TheMasculineHome) à partir des transcriptions vidéo.

**Méthode** :
1. Récupération de la liste des vidéos via l'API Supadata.ai
2. Extraction des transcriptions de 40 vidéos
3. Analyse détaillée pour identifier les produits avec citations exactes du YouTuber
4. Recherche de liens d'achat livrables en France

**Résultats** :
- 40 vidéos analysées
- 85+ produits identifiés avec descriptions exactes
- Catégories : Textiles, Bougies, Mobilier, Tapis, Éclairage, Bar, Décoration, Plantes, Peintures
- Prix de 12€ à 2,480€
- Tous les liens sont livrables en France

**Fichiers** :
- `researches/masculine-home-products/products-table.md` : Tableau complet des produits
- `researches/masculine-home-products/video-list.json` : Liste des 76 vidéos de la chaîne
- `researches/masculine-home-products/transcripts.json` : Transcriptions des 40 vidéos

## Description

Ce dépôt est un espace dédié aux recherches et au développement d'outils par une IA. Il combine :
- **Recherche** : Investigations approfondies sur le web documentées en Markdown
- **Développement d'outils** : Création autonome de projets pour automatiser et améliorer les capacités de recherche

## Technologies utilisées

- Python 3 (scripts d'analyse)
- API Supadata.ai (récupération de données YouTube)
- Markdown (documentation des recherches)
