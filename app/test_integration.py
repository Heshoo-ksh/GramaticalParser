import pytest
from app import app 
from app import views  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_parse_story_with_main_noun(client):
    response = client.post('/parse', json={
        "story": "As a project manager, I need a dashboard to track project progress.",
        "main_noun": "dashboard"
    })
    assert response.status_code == 200

def test_parse_story_without_main_noun(client):
    response = client.post('/parse', json={
        "story": "As a project manager, I need a dashboard to track project progress."
    })
    assert response.status_code == 200

def test_parse_story_noun_data_structure(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    noun_data = response.get_json()['nouns'][0]
    assert all(key in noun_data for key in ['noun', 'associated_nouns', 'associated_verbs'])

def test_spell_check_endpoint_corrects_misspellings(client):
    response = client.post('/spell_check', json={"text": "I need a dasboaard"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["corrected_text"] == "I need a dashboard"

# Test the spell check endpoint with an empty string
def test_spell_check_endpoint_with_empty_string(client):
    response = client.post('/spell_check', json={"text": ""})
    assert response.status_code == 200
    data = response.get_json()
    assert 'corrected_text' in data
    assert data['corrected_text'] == ""

# Test the spell check endpoint with a correct input
def test_spell_check_endpoint_corrects_misspellings(client):
    text = "I neeed a daashboard for tracking projectes"
    response = client.post('/spell_check', json={"text": text})
    assert response.status_code == 200
    data = response.get_json()
    assert 'corrected_text' in data
    corrected_text = data['corrected_text']
    assert corrected_text == "I need a dashboard for tracking projects"

# Test the spell check endpoint with a non-JSON payload
def test_spell_check_endpoint_with_non_json_payload(client):
    response = client.post('/spell_check', data="This is not JSON")
    assert response.status_code == 415

# Test the parse story endpoint with a non-JSON payload
def test_parse_story_with_non_json_payload(client):
    response = client.post('/parse', data="This is not JSON")
    assert response.status_code == 415

# Test the parse story endpoint without a main noun
def test_parse_story_without_main_noun(client):
    story = "As a project manager, I need to track project progress."
    response = client.post('/parse', json={"story": story})
    assert response.status_code == 200
    
# Test the parse story endpoint with an empty story
def test_parse_story_with_empty_story(client):
    response = client.post('/parse', json={"story": "", "main_noun": "dashboard"})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Story text must be provided!'

# Test the parse story endpoint when no main noun is provided
def test_parse_story_auto_determines_main_noun_when_none_provided(client):
    story = "As a project manager, I need to track project progress."
    response = client.post('/parse', json={"story": story})
    assert response.status_code == 200
    data = response.get_json()
    assert 'nouns' in data
    assert len(data['nouns']) > 0
    found_main_noun = data['nouns'][0]['noun']
    assert found_main_noun == 'project', "The main noun should be 'project' when none is provided"

# Test the parse story endpoint finds associated nouns correctly with the main noun provided
def test_parse_story_finds_associated_nouns_correctly_without_main_noun(client):
    story = "As a project manager, I need a dashboard to track project progress."
    response = client.post('/parse', json={"story": story})
    data = response.get_json()
    associated_nouns = data['nouns'][0]['associated_nouns']
    expected_nouns = ['project manager', 'project progress', 'dashboard']  
    for noun in expected_nouns:
        assert noun in associated_nouns

# Test the parse story endpoint finds associated nouns correctly without the main noun provided
def test_parse_story_finds_associated_nouns_correctly_with_main_noun(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    data = response.get_json()
    associated_nouns = data['nouns'][0]['associated_nouns']
    expected_nouns = ['project manager', 'project progress']  
    for noun in expected_nouns:
        assert noun in associated_nouns

# Test the parse story endpoint finds associated verbs correctly without the main noun provided
def test_parse_story_finds_associated_verbs_correctly_without_main_noun(client):
    story = "As a project manager, I need a dashboard to track project progress."
    response = client.post('/parse', json={"story": story})
    data = response.get_json()
    associated_verbs = data['nouns'][0]['associated_verbs']
    expected_verbs = ['need dashboard', 'track progress'] 
    for verb in expected_verbs:
        assert verb in associated_verbs

# Test the parse story endpoint finds associated verbs correctly with the main noun provided
def test_parse_story_finds_associated_verbs_correctly_with_main_noun(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    data = response.get_json()
    associated_verbs = data['nouns'][0]['associated_verbs']
    expected_verbs = ['need dashboard', 'track progress'] 
    for verb in expected_verbs:
        assert verb in associated_verbs

# Test the parse story endpoint with a well-defined input for the main noun
def test_parse_story_with_main_noun(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    assert response.status_code == 200
    data = response.get_json()
    assert 'nouns' in data
    assert isinstance(data['nouns'], list)
    assert len(data['nouns']) > 0
    assert data['nouns'][0]['noun'] == main_noun

# Test the parse story endpoint for finding expected associated nouns
def test_parse_story_finds_expected_associated_nouns(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    data = response.get_json()
    expected_nouns = ['project progress', 'project manager']
    associated_nouns = data['nouns'][0]['associated_nouns']
    for noun in expected_nouns:
        assert noun in associated_nouns

# Test the parse story endpoint for finding expected associated verbs
def test_parse_story_finds_expected_associated_verbs(client):
    story = "As a project manager, I need a dashboard to track project progress."
    main_noun = "dashboard"
    response = client.post('/parse', json={"story": story, "main_noun": main_noun})
    data = response.get_json()
    expected_verbs = ['need dashboard', 'track progress']
    associated_verbs = data['nouns'][0]['associated_verbs']
    for verb in expected_verbs:
        assert verb in associated_verbs

