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
    # Extract the story text from the request
    data = request.json
    user_story = data['story']
    
    # Perform spell check
   # spell_checked_story = spell_check(user_story)

    # Process the text with SpaCy
  #  doc = nlp(spell_checked_story)

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
    

@app.route('/spell_check', methods=['POST'])
def spell_check():
    # get the user story into the here to get checked for misspelling 
    data = request.json
    user_story = data['text']

    # Perform spell check
    corrected_text = spell_check_text(user_story)

    return jsonify({"corrected_text": corrected_text})

def spell_check_text(text):
    # Split the text into words
    words = text.split()

    # Perform spell check and get corrected words
    corrected_words = [spell.correction(word) for word in words]

    # Join the corrected words back into a sentence
    corrected_text = ' '.join(corrected_words)

    return corrected_text