# Photos d'exemple du simulateur de covering

Les photos de ce dossier apparaissent dans la rubrique **Photos d'exemple** de
[covering-colonnes.html](../covering-colonnes.html). Un clic sur une vignette
applique la photo à la face sélectionnée, ou à tout le tour.

## Ajouter ou retirer une photo

1. Déposer la photo dans ce dossier `exemples-covering/` (ou la supprimer).
2. Faire un commit et un push sur la branche `main`.
3. Attendre 1 à 2 minutes : l'Action **Galerie covering** (onglet *Actions*
   du dépôt) met à jour `galerie.json` et crée la vignette dans `vignettes/`.
   GitHub Pages republie ensuite le site.
4. Avant de modifier à nouveau le dépôt sur l'ordinateur, récupérer ce commit
   automatique (*Fetch / Pull origin* dans GitHub Desktop).

Le titre et le crédit sont déduits du nom de fichier, sur le modèle
`Titre_de_la_photo-Photographe_-__Source-12345.jpg`. Pour les corriger
(accents, majuscules) ou ajouter une description, modifier `titre`, `credit` ou
`description` dans `galerie.json` : ces valeurs ne sont jamais écrasées. On
peut aussi y changer l'ordre des photos. Ne pas modifier les autres champs, ils
sont recalculés.

## Formats et poids conseillés

- **Formats** : JPG (conseillé), PNG ou WebP. Les formats HEIC (iPhone), TIFF
  ou RAW ne sont pas lus par les navigateurs : les convertir en JPG.
- **Définition** : au moins 4 500 px de large pour une face ; pour tout le
  tour, un panoramique d'environ 6 000 × 3 000 px (colonne 4 m³) ou
  8 000 × 3 000 px (5 m³). L'outil affiche les dpi obtenus : il en faut 70 à 100.
- **Poids** : 2 à 10 Mo par photo (JPG qualité 85-90). La photo complète est
  téléchargée au clic : au-delà de 20 Mo, l'attente devient longue.
- **Limites GitHub** : 100 Mo maximum par fichier (refusé au-delà), et un
  dépôt GitHub Pages doit rester sous 1 Go au total.

## Droits d'auteur et droit à l'image

Le dépôt et le site sont **publics** : toute photo déposée ici est visible et
téléchargeable par n'importe qui.

- N'ajouter que des photos dont NCPA détient les droits, ou dont la licence
  autorise une diffusion publique, et indiquer le crédit demandé par l'auteur.
- Pour les photos issues d'une photothèque (par exemple celle de Normandie Pays
  d'Auge), vérifier que les conditions d'utilisation autorisent cette mise en
  ligne.
- Une personne reconnaissable sur une photo doit avoir donné son accord écrit
  pour sa diffusion. À défaut, choisir une autre photo.
- Pour retirer une photo, la supprimer du dossier suffit pour le site, mais
  elle reste dans l'historique Git du dépôt.
