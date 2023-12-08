from app import app
from flask import request, jsonify
import spacy
from spellchecker import SpellChecker
from app.models import NounObject

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/parse', methods=['POST'])
def parse_story():
    data = request.json
    user_story = data['story']
    main_noun_input = data['main_noun']
    
    doc = nlp(user_story)
    main_noun_obj = None

    # Find the main noun in the document
    for token in doc:
        if token.text.lower() == main_noun_input.lower():
            main_noun_obj = NounObject(token.text)
            break

    if main_noun_obj:
        for token in doc:
            # Check for direct and indirect associations with the main noun
            if token.head.text == main_noun_obj.noun or main_noun_obj.noun in [ancestor.text for ancestor in token.ancestors]:
                if token.pos_ == 'VERB':
                    main_noun_obj.add_associated_verb(token.text)
                elif token.pos_ == 'NOUN' and token.text.lower() != main_noun_obj.noun.lower():
                    # Check for compound nouns
                    if token.dep_ == 'compound':
                        compound_noun = token.text + ' ' + token.head.text
                        main_noun_obj.add_associated_noun(compound_noun)
                    else:
                        main_noun_obj.add_associated_noun(token.text)

    response = {
        "nouns": [main_noun_obj.to_dictionary()] if main_noun_obj else []
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