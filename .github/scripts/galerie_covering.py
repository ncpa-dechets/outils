"""Met à jour exemples-covering/galerie.json et les vignettes de la galerie.

Lancé par la GitHub Action « Galerie covering » à chaque push qui touche
le dossier exemples-covering/. Peut aussi se lancer à la main :
    python .github/scripts/galerie_covering.py

Règles :
- chaque photo du dossier (jpg, jpeg, png, webp) a une entrée dans la liste ;
- les entrées des photos retirées du dossier sont supprimées, ainsi que
  leurs vignettes ;
- titre, crédit et description saisis à la main ne sont jamais écrasés :
  ils ne sont déduits du nom de fichier que s'ils sont absents ;
- une vignette d'environ 400 px est créée dans exemples-covering/vignettes/,
  et recréée seulement si la photo a changé (empreinte).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

RACINE = Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "exemples-covering"
VIGNETTES = DOSSIER / "vignettes"
LISTE = DOSSIER / "galerie.json"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
TAILLE_VIGNETTE = 400          # px, plus grand côté
AIDE = ("Liste mise à jour automatiquement à chaque push. Vous pouvez modifier "
        "« titre », « credit » et « description » (et l'ordre des photos) : "
        "ces valeurs ne sont jamais écrasées.")


def nettoyer(txt):
    txt = re.sub(r"[_\s]+", " ", txt).strip(" -")
    # élisions perdues dans les noms de fichiers : « d Auge » -> « d'Auge »
    txt = re.sub(r"\b([dlDL]) (?=[A-Za-zÀ-ÿ])", r"\1'", txt)
    return txt[:1].upper() + txt[1:]


def deduire(nom):
    """Titre et crédit déduits du nom : « Titre-Photographe_-__Source-12345.jpg »."""
    morceaux = [m for m in Path(nom).stem.split("-") if m.strip(" _")]
    if len(morceaux) > 1 and morceaux[-1].strip(" _").isdigit():
        morceaux = morceaux[:-1]
    morceaux = [nettoyer(m) for m in morceaux] or [nettoyer(Path(nom).stem)]
    return morceaux[0], " / ".join(morceaux[1:])


def empreinte(chemin):
    h = hashlib.sha1()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()[:12]


def main():
    if not DOSSIER.is_dir():
        sys.exit(f"Dossier introuvable : {DOSSIER}")
    ancien = {}
    if LISTE.exists():
        try:
            donnees = json.loads(LISTE.read_text(encoding="utf-8"))
            photos = donnees.get("photos", []) if isinstance(donnees, dict) else donnees
            ancien = {p["fichier"]: p for p in photos if isinstance(p, dict) and p.get("fichier")}
        except (ValueError, KeyError) as e:
            sys.exit(f"galerie.json illisible, corrigez-le avant de relancer : {e}")

    fichiers = sorted((p for p in DOSSIER.iterdir()
                       if p.is_file() and p.suffix.lower() in EXTENSIONS),
                      key=lambda p: p.name.lower())
    noms = {p.name for p in fichiers}
    # ordre : d'abord celui de la liste existante (modifiable à la main), puis les nouvelles
    ordre = [n for n in ancien if n in noms] + [p.name for p in fichiers if p.name not in ancien]

    VIGNETTES.mkdir(exist_ok=True)
    gardees, sortie, vus = set(), [], {}
    for nom in ordre:
        src = DOSSIER / nom
        e = dict(ancien.get(nom, {}))
        titre_auto, credit_auto = deduire(nom)
        if not e.get("titre"):
            n = vus.get(titre_auto, 0) + 1
            e["titre"] = titre_auto if n == 1 else f"{titre_auto} ({n})"
        vus[titre_auto] = vus.get(titre_auto, 0) + 1
        if "credit" not in e:
            e["credit"] = credit_auto
        e.setdefault("description", "")

        emp = empreinte(src)
        vig = e.get("vignette", "")
        manuelle = vig and not vig.startswith("vignettes/") and (DOSSIER / vig).is_file()
        if not manuelle:
            vig = f"vignettes/{src.stem}.jpg"
            if sum(1 for p in fichiers if p.stem == src.stem) > 1:
                vig = f"vignettes/{src.stem}_{src.suffix.lstrip('.').lower()}.jpg"
            gardees.add(vig)
        cible = DOSSIER / vig
        try:
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im)
                largeur, hauteur = im.size
                if not manuelle and (e.get("empreinte") != emp or not cible.is_file()):
                    im.thumbnail((TAILLE_VIGNETTE, TAILLE_VIGNETTE), Image.LANCZOS)
                    im.convert("RGB").save(cible, "JPEG", quality=80, optimize=True, progressive=True)
                    print(f"vignette : {vig}")
        except OSError as err:
            print(f"ATTENTION, photo illisible ignorée : {nom} ({err})")
            continue
        poids = src.stat().st_size / 1e6
        if poids > 50:
            print(f"ATTENTION : {nom} pèse {poids:.0f} Mo (GitHub refuse au-delà de 100 Mo)")

        sortie.append({
            "fichier": nom,
            "titre": e["titre"],
            "credit": e["credit"],
            "description": e["description"],
            "vignette": vig,
            "largeur": largeur,
            "hauteur": hauteur,
            "empreinte": emp,
        })

    for v in VIGNETTES.glob("*.jpg"):
        if f"vignettes/{v.name}" not in gardees:
            v.unlink()
            print(f"vignette supprimée : {v.name}")

    texte = json.dumps({"_aide": AIDE, "photos": sortie}, ensure_ascii=False, indent=2) + "\n"
    if not LISTE.exists() or LISTE.read_text(encoding="utf-8") != texte:
        LISTE.write_text(texte, encoding="utf-8", newline="\n")
        print(f"galerie.json mis à jour : {len(sortie)} photo(s)")
    else:
        print(f"galerie.json inchangé : {len(sortie)} photo(s)")


if __name__ == "__main__":
    main()
