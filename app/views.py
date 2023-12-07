from app import app
from flask import request, jsonify
import spacy
from spellchecker import SpellChecker

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/parse', methods=['POST'])
def parse_story():

    data = request.json
    user_story = data['story']
    
    doc = nlp(user_story)
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    verbs = [token.text for token in doc if token.pos_ == 'VERB']
    response = {
        "nouns": nouns,
        "verbs": verbs
    }
    return jsonify(response)
    

@app.route('/spell_check', methods=['POST'])
def spell_check():

    data = request.json
    user_story = data['text']
    corrected_text = spell_check_text(user_story)

    return jsonify({"corrected_text": corrected_text})

def spell_check_text(text):

    words = text.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_text = ' '.join(corrected_words)

    return corrected_text