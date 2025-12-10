# Plan d'analyse - The Masculine Home YouTube Channel

## Objectif
Analyser les vidéos de la chaîne YouTube "The Masculine Home" pour extraire tous les produits mentionnés, puis créer un tableau avec les informations d'achat.

## Chaîne cible
- **URL** : https://www.youtube.com/@TheMasculineHome
- **Fondateur** : Chaudry Ghafoor
- **Thème** : Décoration intérieure masculine

---

## Étapes du plan

### Étape 1 : Récupérer la liste des vidéos
**Statut** : ✅ Terminé

**Solution retenue** : API Supadata.ai
- Clé API fournie par l'utilisateur
- Endpoint : `GET https://api.supadata.ai/v1/youtube/channel/videos`
- **Résultat** : 76 vidéos + 12 shorts identifiés

**Fichier de sortie** : `video-list.json`

---

### Étape 2 : Récupérer les transcriptions
**Statut** : ✅ Terminé (partiel)

**Solution retenue** : API Supadata.ai
- Script : `tools/youtube-analyzer/fetch_transcripts.py`
- Endpoints utilisés :
  - `/youtube/video` pour les métadonnées
  - `/youtube/transcript` pour les transcriptions
- **Résultat** : 40/76 vidéos avec transcriptions (rate limit atteint)

**Fichier de sortie** : `transcripts.json` (1.6 Mo)

---

### Étape 3 : Analyser les transcriptions
**Statut** : ✅ Terminé

**Méthode** :
- Analyse automatisée des mots-clés produits
- Extraction des catégories : mobilier, tapis, éclairage, textiles, bougies, bar
- **Constat** : Les vidéos mentionnent des catégories de produits, pas de marques spécifiques

**Fichier de sortie** : `products-list.md`

---

### Étape 4 : Recherche des produits et création du tableau
**Statut** : ✅ Terminé (première phase)

**Informations collectées** :
- 85+ produits identifiés avec liens d'achat
- 10 catégories : Mobilier, Tapis, Éclairage, Textile, Bougie, Bar, Déco, Plantes, Peintures, Matériaux
- Prix de 12€ à 2480€
- Tous livrables en France

**Fichier de sortie** : `products-table.md`

---

### Étape 5 : Compléter les produits manquants
**Statut** : ✅ Terminé

**Produits ajoutés** :

#### BOUGIES (2 produits) ✅
- [x] Bougie Balsam & Cedar - Notino - Milkhouse Candle
- [x] Bougie Fresh Cut Pine - Durance

#### VERDURE NATURELLE (5 produits) ✅
- [x] Branches eucalyptus séché - France Fleurs
- [x] Branches sapin naturel - Sapins-Noel.fr
- [x] Branches olivier décoration - France Fleurs
- [x] Pommes de pin naturelles - Zôdio
- [x] Branches magnolia artificiel - Artiplantes

#### DÉCORATION (7 produits) ✅
- [x] Boîte bois sculpté - Etsy France
- [x] Cloche antique laiton - Materiaux Anciens Bidal
- [x] Livres reliés cuir - La Librairie Antique
- [x] Serre-livres tête de cheval - Maisons du Monde
- [x] Serre-livres colonne corinthien - De Bejarry
- [x] Boussole vintage laiton - Les Baroudeurs

#### BAR ACCESSOIRES (4 produits) ✅
- [x] Match striker - Amazon.fr
- [x] Porte-bouteille cuir vin - So-BBQ
- [x] Serviettes lin table - Le Jacquard Français
- [x] Tire-bouchon manche bois - Ligne W Prestige

#### TEXTILES (1 produit) ✅
- [x] Rideaux lin naturel - La Draperie Française

#### REVÊTEMENTS MURAUX (3 produits) ✅
- [x] Fausses poutres plafond espresso - ExpertDecor
- [x] Papier peint lin grasscloth - La Maison Bineau
- [x] Papier peint effet cuir - 4Murs

#### ACCESSOIRES PERSONNELS (2 produits) ✅
- [x] Vide-poche bois plateau - Faugier France
- [x] Carnet cuir avec stylo - Louise Carmen

**Total produits ajoutés** : 24

---

## Structure des fichiers

```
researches/masculine-home-products/
├── PLAN.md                 # Ce fichier (plan de travail)
├── video-list.json         # Liste des vidéos de la chaîne (76 vidéos)
├── transcripts.json        # Transcriptions complètes (40 vidéos)
├── products-list.md        # Liste brute des produits identifiés
└── products-table.md       # Tableau final avec prix et liens
```

---

## Journal de progression

### 2024-12-09
- [x] Création du plan de travail
- [x] Installation des outils (yt-dlp, youtube-transcript-api, ytpl, supadata)
- [x] Étape 1 : Liste des vidéos récupérée via Supadata API
- [x] Étape 2 : Transcriptions récupérées (40/76 vidéos)
- [x] Étape 3 : Analyse des transcriptions terminée
- [x] Étape 4 : Tableau final créé avec 22 produits et liens d'achat

---

## Notes techniques

### Contraintes de l'environnement
- Proxy avec certificat auto-signé bloquant l'accès direct à YouTube
- Solution : API Supadata.ai (service tiers)

### Outils utilisés
- `supadata.ai` API - pour vidéos et transcriptions
- Python pour le scripting
- Recherche web pour les prix et liens

### Résumé des résultats
- **Vidéos analysées** : 40
- **Produits identifiés** : 22
- **Catégories** : 6 (Mobilier, Tapis, Éclairage, Textile, Bougie, Bar)
- **Gamme de prix** : 20€ - 2480€
