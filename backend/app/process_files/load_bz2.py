import bz2
import json
import logging
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import wikitextparser as wtp

logger = logging.getLogger(__name__)

DUMP_URL_TEMPLATE = (
    "https://dumps.wikimedia.org/eswiki/{date}/"
    "eswiki-{date}-pages-articles-multistream.xml.bz2"
)

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def _get_plain_text(revision, ns):
    text_el = revision.find(f"{ns}text")
    if text_el is None or text_el.text is None:
        return None
    parsed = wtp.parse(text_el.text)
    for ref in parsed.get_tags("ref"): # Delete references
        ref.contents = ""
    return parsed.plain_text().strip()


def _download_bz2(date: str) -> Path:
    bz2_path = DATA_DIR / f"eswiki-{date}-pages-articles-multistream.xml.bz2"
    if bz2_path.exists():
        logger.info("BZ2 already cached: %s", bz2_path)
        return bz2_path

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    url = DUMP_URL_TEMPLATE.format(date=date)
    logger.info("Downloading %s", url)
    urllib.request.urlretrieve(url, bz2_path)
    logger.info("Download complete: %s", bz2_path)
    return bz2_path


def _process(stream, output_path: Path) -> tuple[int, int]:
    total, skipped = 0, 0
    context = iter(ET.iterparse(stream, events=("start", "end")))
    _, root = next(context)
    ns = root.tag.split("}")[0] + "}"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("[\n")
        first = True
        for event, elem in context:
            if event == "end" and elem.tag == f"{ns}page":
                title_el = elem.find(f"{ns}title")
                revision = elem.find(f"{ns}revision")
                if revision is None:
                    skipped += 1
                else:
                    rev_id_el = revision.find(f"{ns}id")
                    text = _get_plain_text(revision, ns)
                    if text is None:
                        skipped += 1
                    else:
                        if not first:
                            f.write(",\n")
                        json.dump({
                            "revision_id": rev_id_el.text if rev_id_el is not None else None,
                            "title": title_el.text if title_el is not None else None,
                            "text": text,
                        }, f, ensure_ascii=False)
                        first = False
                        total += 1
                        if total % 500 == 0:
                            logger.info("Written %d pages...", total)
                elem.clear()
                root.clear()
        f.write("\n]\n")

    return total, skipped


def run(date: str) -> dict:
    """Download, decompress and process an eswiki dump for the given date.

    Args:
        date: Dump date in YYYYMMDD format, e.g. '20260301'.

    Returns:
        Dict with keys: output_path, total_pages, skipped, elapsed_seconds.

    Raises:
        ValueError: If the date format is invalid.
    """
    if not re.fullmatch(r"\d{8}", date):
        raise ValueError(f"Invalid date '{date}': must be 8 digits, e.g. 20260301")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / f"eswiki-{date}-pages-articles.json"

    start = time.time()
    bz2_path = _download_bz2(date)
    with bz2.open(bz2_path, "rb") as stream:
        total, skipped = _process(stream, output_path)
    elapsed = round(time.time() - start, 2)

    logger.info("Done. %d pages written, %d skipped in %ss", total, skipped, elapsed)
    return {
        "output_path": str(output_path),
        "total_pages": total,
        "skipped": skipped,
        "elapsed_seconds": elapsed,
    }