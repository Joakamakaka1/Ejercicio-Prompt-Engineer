"""Genera los dos datasets del Ejercicio 1 a partir de Inside Airbnb (Oporto).

Los CSV originales del curso (`listings1_cleaned.csv` y `Airbnb_reviews_5000.csv`)
no estaban disponibles, así que se reconstruyen con los datos públicos de
Inside Airbnb (https://insideairbnb.com, licencia CC BY 4.0):

- `listings1_cleaned.csv`: anuncios de Oporto con descripción, HTML limpiado y
  solo las columnas útiles para el ejercicio (sin datos del anfitrión).
- `Airbnb_reviews_5000.csv`: las 5.000 reseñas más recientes de esos anuncios,
  sin nombre ni id del revisor.

Uso (desde la raíz del repo):
    uv run python ejercicio-1/scripts/preparar_datos.py
    uv run python ejercicio-1/scripts/preparar_datos.py --raw-dir <carpeta con los .csv.gz>
"""

import argparse
import html
import re
from pathlib import Path

import pandas as pd

SNAPSHOT = "2026-09-19"
BASE_URL = f"https://data.insideairbnb.com/portugal/norte/porto/{SNAPSHOT}/data"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
N_RESENAS = 5000

COLUMNAS_LISTINGS = [
    "id", "name", "description", "neighborhood_overview",
    "neighbourhood_cleansed", "neighbourhood_group_cleansed",
    "property_type", "room_type", "accommodates", "bathrooms_text",
    "bedrooms", "beds", "amenities", "price", "number_of_reviews",
    "review_scores_rating", "review_scores_cleanliness",
    "review_scores_location", "review_scores_value",
]


def limpiar_html(texto):
    """Pasa el HTML de Airbnb (<br />, <b>…</b>, &amp;) a texto plano."""
    if not isinstance(texto, str):
        return texto
    texto = re.sub(r"<br\s*/?>", "\n", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n\s*\n+", "\n", texto)
    return texto.strip()


def origen(raw_dir, nombre):
    if raw_dir:
        return Path(raw_dir) / f"{nombre}.csv.gz"
    return f"{BASE_URL}/{nombre}.csv.gz"


def preparar_listings(raw_dir):
    df = pd.read_csv(origen(raw_dir, "listings"), usecols=COLUMNAS_LISTINGS)
    for col in ["name", "description", "neighborhood_overview"]:
        df[col] = df[col].map(limpiar_html)
    df = df.dropna(subset=["description"])
    df = df[df["description"].str.len() > 0]
    df = df.drop_duplicates(subset=["description"])
    return df[COLUMNAS_LISTINGS].reset_index(drop=True)


def preparar_reviews(raw_dir, ids_listings):
    df = pd.read_csv(origen(raw_dir, "reviews"),
                     usecols=["listing_id", "id", "date", "comments"])
    df = df[df["listing_id"].isin(ids_listings)]
    df["comments"] = df["comments"].map(limpiar_html)
    df = df.dropna(subset=["comments"])
    df = df[df["comments"].str.len() > 0]
    df = df.sort_values(["date", "id"], ascending=False).head(N_RESENAS)
    return df.rename(columns={"id": "review_id"}).reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--raw-dir", help="Carpeta con listings.csv.gz y reviews.csv.gz "
                                          "ya descargados (si no, se leen de la URL).")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    listings = preparar_listings(args.raw_dir)
    listings.to_csv(DATA_DIR / "listings1_cleaned.csv", index=False)
    print(f"listings1_cleaned.csv: {listings.shape}")

    reviews = preparar_reviews(args.raw_dir, set(listings["id"]))
    reviews.to_csv(DATA_DIR / "Airbnb_reviews_5000.csv", index=False)
    print(f"Airbnb_reviews_5000.csv: {reviews.shape} "
          f"({reviews['date'].min()} a {reviews['date'].max()})")


if __name__ == "__main__":
    main()
