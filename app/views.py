from app import app
from flask import request, jsonify
import spacy

nlp = spacy.load("en_core_web_sm")


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/parse', methods=['POST'])
def parse_story():
    # Extract the story text from the request
    data = request.json
    user_story = data['story']

    # Process the text with SpaCy
    doc = nlp(user_story)
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    # Structure the response
    response = {
        "nouns": nouns,
        "verbs": verbs
    }

    # Return the response in JSON format
    return jsonify(response)
