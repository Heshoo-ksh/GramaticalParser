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
        compound_nouns = set()  # To track compound nouns
        individual_nouns = set()  # To track individual nouns

        # First pass: Identify and store compound nouns
        for token in doc:
            if token.dep_ == 'compound' and token.head.pos_ == 'NOUN':
                compound_noun = token.text + ' ' + token.head.text
                compound_nouns.add(compound_noun.lower())

        # Second pass: Collect associations avoiding duplicates
        for token in doc:
            if token.pos_ == 'VERB' and (token.head.text == main_noun_obj.noun or main_noun_obj.noun in [ancestor.text for ancestor in token.ancestors]):
                verb_lemma = token.lemma_
                # Use SpaCy's vocabulary to check if lemma is a valid English word
                if verb_lemma in nlp.vocab:
                    main_noun_obj.add_associated_verb(token.lemma_)
                else:
                    main_noun_obj.add_associated_verb(token.text)
            elif token.pos_ == 'NOUN' and token.text.lower() != main_noun_obj.noun.lower():
                if not any(token.text.lower() in cn for cn in compound_nouns):
                    individual_nouns.add(token.text.lower())

        # Add compound nouns and individual nouns to the associations
        for cn in compound_nouns:
            main_noun_obj.add_associated_noun(cn)
        for noun in individual_nouns:
            main_noun_obj.add_associated_noun(noun)

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