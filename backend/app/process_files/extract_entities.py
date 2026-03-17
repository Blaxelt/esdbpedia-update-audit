
def extract_entities(parsed):
    entities = []

    for link in parsed.wikilinks:
        surface = link.text if link.text else link.title
        if not surface:
            continue

        entities.append(str(surface))

    return entities