from pathlib import Path

wikipedia_index: dict[str, set[str]] = {"es": set(), "en": set()}

ROOT_DIR = Path(__file__).parents[3]

INDEX_FILES = {
    "es": ROOT_DIR / "index" / "eswiki-20260301-pages-articles-multistream-index.txt",
    "en": ROOT_DIR / "index" / "enwiki-20260301-pages-articles-multistream-index.txt",
}

def load_index(lang: str):
    path = Path(INDEX_FILES[lang])
    print(f"[{lang}] Cargando índice desde {path}...")

    titles = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(":", 2)
            if len(parts) == 3:
                titles.add(parts[2].replace(" ", "_"))

    wikipedia_index[lang] = titles
    print(f"[{lang}] {len(titles):,} títulos cargados")

def load_all():
    for lang in ["es", "en"]:
        load_index(lang)