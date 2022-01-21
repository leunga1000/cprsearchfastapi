from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_policies():
    response = client.get("/policy")
    print(response)
    assert response.status_code == 200
    assert len(response.json()) > 100

def test_read_policy():
    response = client.get("/policy/10088")
    assert response.status_code == 200
    assert response.json() == {
	    "id": "10088", 
	    "title": "Circular economy promotion law", 
	    "description_text": "This law promotes the development of a circular economy, aims to improve resource usage and protect the environment. It notably seeks to enhance energy efficiency, increase the role of renewable energy sources\xa0", 
	    "sectors": [
	        "Industry", 
	        "Agriculture", 
	        "Economy-wide"
	    ]
	}


def test_search_policy():
    response = client.get('/policy/search/environment%20fossil')
    assert response.status_code == 200
    for d in response.json():
    	assert 'environment' in d['description_text'].lower() or 'fossil' in d['description_text'].lower()
    	assert 'jaccard_similarity' in d and d['jaccard_similarity'] > 0
