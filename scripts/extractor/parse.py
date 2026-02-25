import wikitextparser as wtp
import xml.etree.ElementTree as ET
import time
import os
import json

def get_plain_text(revision, ns):
    text_element = revision.find(f'{ns}text')
    if text_element is None or text_element.text is None:
        return None
    parsed = wtp.parse(text_element.text)
    references = parsed.get_tags('ref')
    for ref in references:
        ref.contents = ''
    return parsed.plain_text().strip()

def process_all_pages(filepath, output_path):
    total_pages = 0
    skipped = 0

    # Use iterparse for memory-efficient streaming
    context = ET.iterparse(filepath, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)
    ns = root.tag.split('}')[0] + '}'

    # Open file for streaming
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("[\n")
        is_first = True

        for event, elem in context:
            if event == 'end' and elem.tag == f'{ns}page':
                title_el = elem.find(f'{ns}title')
                revision = elem.find(f'{ns}revision')

                if revision is None:
                    skipped += 1
                else:
                    rev_id_el = revision.find(f'{ns}id')
                    text = get_plain_text(revision, ns)

                    if text is None:
                        skipped += 1
                    else:
                        # Rebuild your results dictionary
                        record = {
                            "id": rev_id_el.text if rev_id_el is not None else None,
                            "title": title_el.text if title_el is not None else None,
                            "text": text
                        }

                        # Stream to JSON directly
                        if not is_first:
                            f.write(",\n")
                        f.write(json.dumps(record, ensure_ascii=False, indent=2))
                        is_first = False
                        
                        total_pages += 1

                # Clean up memory for the node we just processed
                elem.clear()
                root.clear()

        f.write("\n]\n")

    return total_pages, skipped

def print_stats(start_time, total_pages, skipped, input_path, output_path):
    elapsed_sec  = time.time() - start_time
    elapsed_hour = elapsed_sec / 3600
    pages_hour   = total_pages / elapsed_hour if elapsed_hour > 0 else 0
    input_mb     = os.path.getsize(input_path) / 1024 / 1024
    output_mb    = os.path.getsize(output_path) / 1024 / 1024

    print("\n========== STATS ==========")
    print(f"Pages processed  : {total_pages}")
    print(f"Pages skipped    : {skipped}")
    print(f"Time elapsed     : {elapsed_sec:.2f} seconds")
    print(f"Speed            : {pages_hour:,.0f} pages/hour")
    print(f"Input file size  : {input_mb:.2f} MB")
    print(f"Output file size : {output_mb:.2f} MB")
    if input_mb > 0:
        print(f"Size reduction   : {((input_mb - output_mb) / input_mb) * 100:.1f}%")
    print("===========================\n")

def run(filepath, output_path="output.json"):
    start_time = time.time()
    
    total_pages, skipped = process_all_pages(filepath, output_path)

    print_stats(start_time, total_pages, skipped, filepath, output_path)

FILEPATH = './eswiki-20260201-pages-articles-multistream1.xml-p1p159400'
OUTPUT_PATH = "output.json"

run(FILEPATH, OUTPUT_PATH)