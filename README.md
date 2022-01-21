### Summary

Thought this would be a simpler implementation rather than Django, so thought I'd take the opportunity to use FastAPI for a slightly larger project. The data is stored in memory, so could be the basis of a sharded application, but may want to drop to a lower level language. Otherwise look into scaled DBs e.g. Redis/ES/Aurora

### Installation

Make virtual environment...
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md  # for spacy support
uvicorn main:app --reload
```

```windows
docker build -t cpr2 . && docker run -p 8000:8000 -v %cd%:/usr/src/app cpr2
```
### Hello World
[http://127.0.0.1:8000/]

### Docs
[http://127.0.0.1:8000/docs]
[http://127.0.0.1:8000/redoc]

### Policies
[http://127.0.0.1:8000/policy]
[http://127.0.0.1:8000/policy/10088]
[http://localhost:8000/policy/search/environment]

If you're not on Windows!
[http://localhost:8000/policy/spacy_search/environment]

### Tests
```bash
pytest tests/tests.py
```

### Things to do with more time.
Complete tests
Put/Patch/Delete
Pydantic/ORM etc
tfidf maybe?
Store vectors
NLP models, Bert/Google Universal Sentence Encoder?

