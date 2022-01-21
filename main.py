from functools import lru_cache
from fastapi import FastAPI, Response, status
from data import data, create_policy
from utils import PrettyJSONResponse, transform_text, spacy_nlp
""" run with uvicorn main:app --reload """

app = FastAPI()

DEF_KEYS = ['id', 'title', 'description_text', 'sectors']

@lru_cache(maxsize=None)
def cached_spacy_nlp(s: str):
    return spacy_nlp(s)

def output(d: dict, ks=DEF_KEYS):
    return {k: v for k, v  in d.items() if k in ks}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/policy", response_class=PrettyJSONResponse)
async def policy():
    return [output(d) for d in data]

@app.get("/policy/{_id}", response_class=PrettyJSONResponse)
async def read_policy(_id, response: Response):
    print(data[1])
    ks = ['id', 'title', 'description_text', 'sectors']
    for d in data:
        if d['id'] == _id:
            print(d)
            return output(d)
    response.status_code = 404
    return {'id': 'not found'}

@app.post("/policy/")
async def create_policy_endpoint(policy: dict):
    item_dict = item.dict()
    for k in DEF_KEYS:
        if k not in item_dict:
            raise ValueError(f'{k} missing')
    policy = create_policy(item_dict['id'], item_dict['title'], 
                           item_dict['sectors'], item['description_text'])
    data.append(policy)
    return policy

@app.put("/policy/{_id}", response_class=PrettyJSONResponse)
async def policy_item_update(_id, policy: dict):
    ks = ['id', 'title', 'description_text', 'sectors']
    for d in data:
        if d['id'] == _id:
            d.update(policy)
            return output(d)

@app.get("/policy/search/{search_terms}", response_class=PrettyJSONResponse)
async def policy_search(search_terms):
    sts = set(transform_text(search_terms).split())
    def get_search_data():
        for d in data:
            intersection = sts.intersection(d['terms'])
            if not intersection:
                continue
            union_length = len((sts.union(d['terms'])))
            d['jaccard_similarity'] = len(intersection) / union_length if union_length else 0.0
            yield d
    output_data = [output(d, DEF_KEYS + ['jaccard_similarity']) for d in get_search_data()]
    ordering = 'jaccard_similarity'
    return sorted(output_data, key=lambda k: (k[ordering], ), reverse=True)


@app.get("/policy/spacy_search/{search_terms}", response_class=PrettyJSONResponse)
async def policy_spacy_search(search_terms, response: Response):
    if not spacy_nlp:
        response.status_code = 400
        return {'error': 'spacy not available'}
    
    search_terms_nlp = spacy_nlp(search_terms)        
    sts = set(transform_text(search_terms).split())
    
    def get_spacy_search_data():
        for d in data:
            intersection = sts.intersection(d['terms'])
            if not intersection:
                continue
            # Can preload nlp at server start
            d['spacy_similarity'] = search_terms_nlp.similarity(cached_spacy_nlp(d['description_text']))
            yield d
    output_data = [output(d, DEF_KEYS + ['spacy_similarity']) for d in get_spacy_search_data()]
    ordering = 'spacy_similarity'
    return sorted(output_data, key=lambda k: (k[ordering], ), reverse=True)
