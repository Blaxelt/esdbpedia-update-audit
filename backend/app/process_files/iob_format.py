import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("es_core_news_sm")

def extract_entities(parsed):
    entities = []

    for link in parsed.wikilinks:
        surface = link.text if link.text else link.title
        if not surface:
            continue

        entities.append(str(surface))

    return entities

def bio_from_text(text, entities):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    labels = ["O"] * len(tokens)

    matcher = PhraseMatcher(nlp.vocab, attr="ORTH")
    patterns = []
    for ent in entities:
        pattern = nlp.make_doc(ent)
        if len(pattern) > 0:
            patterns.append(pattern)
    if patterns:
        matcher.add("ENT", patterns)

    matches = matcher(doc)

    # Sort by start position and deduplicate overlapping spans
    # (keep longest match when spans overlap)
    spans = [(start, end) for _, start, end in matches]
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))

    taken = set()
    for start, end in spans:
        if any(i in taken for i in range(start, end)):
            continue
        labels[start] = "B-ENT"
        for j in range(start + 1, end):
            labels[j] = "I-ENT"
        taken.update(range(start, end))

    return tokens, labels