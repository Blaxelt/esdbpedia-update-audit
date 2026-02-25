import wikitextparser as wtp
import xml.etree.ElementTree as ET

def load_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = root.tag.split('}')[0] + '}'
    return root, ns

def find_page_by_revision_id(root, ns, target_id):
    for page in root.iter(f'{ns}page'):
        revision = page.find(f'{ns}revision')
        if revision is None:
            continue
        revision_id = revision.find(f'{ns}id')
        if revision_id is None:
            continue
        if revision_id.text == str(target_id):
            return page, revision
    return None, None


def get_plain_text(revision, ns):
    text_element = revision.find(f'{ns}text')
    if text_element is None or text_element.text is None:
        return None
    parsed = wtp.parse(text_element.text)
    references = parsed.get_tags('ref')
    for ref in references:
        ref.contents = ''
    return parsed.plain_text().strip()


def search_by_revision_id(filepath, target_id):
    root, ns = load_xml(filepath)

    page, revision = find_page_by_revision_id(root, ns, target_id)

    if page is None:
        print(f"Error: revision ID '{target_id}' not found in the dump.")
        return None

    text = get_plain_text(revision, ns)
    if text is None:
        print("Error: page has no text content.")
        return None

    return text


FILEPATH = './eswiki-20260201-pages-articles-multistream1.xml-p1p159400'
TARGET_REVISION_ID = "171311417"

result = search_by_revision_id(FILEPATH, TARGET_REVISION_ID)
if result:
    print(result)