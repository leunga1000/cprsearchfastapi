from utils import transform_text
import csv

def create_policy(l):
    _id, title, sectors, text = l
    words_only_text = transform_text(text)
    unique_words = set(words_only_text.split())
    sectors = sectors.split(';')
    return dict(id=_id,
             title=title,
             description_text=text,
             terms=unique_words,
             sectors = sectors)

def ingest():
    with open('cpr-task_1-full.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        next(reader)
        for l in reader:
            yield create_policy(l)


data = list(ingest())