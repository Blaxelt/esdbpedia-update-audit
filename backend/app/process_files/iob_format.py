import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("es_core_news_sm")

def extract_entities(parsed):
    entities = []

    for link in parsed.wikilinks:
        surface = link.text if link.text else link.title
        if not surface:
            continue

        entities.append({
            "surface": str(surface)
        })

    return entities

def bio_from_text(text, entities):
    tokens = text.split()
    labels = ["O"] * len(tokens)

    for ent in entities:
        words = ent["surface"].split()

        for i in range(len(tokens)):
            if tokens[i:i+len(words)] == words:
                labels[i] = "B-ENT"
                for j in range(1, len(words)):
                    labels[i+j] = "I-ENT"

    return tokens, labels