from app import app
from flask import request, jsonify
from spellchecker import SpellChecker
from app.models import NounObject
from spacy.matcher import PhraseMatcher
import spacy
import nltk

nltk.download('words')
nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

def is_valid_english_word(word):
    return word.lower() in set(nltk.corpus.words.words())

def find_associated_verbs(doc, main_noun_token):
    verbs = set()
    for token in doc:
        if token.pos_ == 'VERB':
            # Direct association: main noun is a child of the verb or vice versa
            if main_noun_token in [child for child in token.children] or token.head == main_noun_token:
                verb_lemma = token.lemma_
                if is_valid_english_word(verb_lemma):
                    verbs.add(verb_lemma)
                else:
                    verbs.add(token.text)
            # Indirect association: verb and main noun are in the same sentence
            elif main_noun_token.sent == token.sent:
                verb_lemma = token.lemma_
                if is_valid_english_word(verb_lemma):
                    verbs.add(verb_lemma)
                else:
                    verbs.add(token.text)
    return list(verbs)



def find_associated_nouns(doc, main_noun_token, compound_nouns):
    nouns = set()
    for token in doc:
        if token.pos_ == 'NOUN' and token.text.lower() != main_noun_token.text.lower():
            is_compound = any(token.text.lower() in cn for cn in compound_nouns)
            if not is_compound:
                nouns.add(token.text)
    return list(nouns)

def find_compound_nouns(doc):
    compounds = set()
    for token in doc:
        if token.dep_ == 'compound' and token.head.pos_ == 'NOUN':
            compound_noun = token.text + ' ' + token.head.text
            compounds.add(compound_noun.lower())
    return compounds

def filter_nouns(individual_nouns, compound_nouns):
    filtered_nouns = set()
    for noun in individual_nouns:
        if not any(noun in cn for cn in compound_nouns):
            filtered_nouns.add(noun)
    return list(filtered_nouns)

def find_main_noun(doc, main_noun_input):
    # Attempt to find the main noun as provided in the input
    main_noun_input = spell_check_word(main_noun_input)

    for token in doc:
        if token.text.lower() == main_noun_input.lower() and token.pos_ == 'NOUN':
            return token

    # Fallback strategy: Use PhraseMatcher to find a similar noun
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns = [nlp.make_doc(main_noun_input)]
    matcher.add('MainNounPattern', patterns)
    matches = matcher(doc)
    
    if matches:
        match_id, start, end = matches[0]
        return doc[start:end]

    # Additional fallback: Use the most frequently mentioned noun
    noun_counts = {}
    for token in doc:
        if token.pos_ == 'NOUN':
            noun_counts[token.text] = noun_counts.get(token.text, 0) + 1
    if noun_counts:
        main_noun = max(noun_counts, key=noun_counts.get)
        return next(token for token in doc if token.text == main_noun)

    return None

@app.route('/parse', methods=['POST'])
def parse_story():
    data = request.json
    user_story = data['story']
    main_noun_input = data.get('main_noun', '')
    
    doc = nlp(user_story)
    main_noun_token = find_main_noun(doc, main_noun_input)
    
    if not main_noun_token:
        return jsonify({"error": "Main noun not found in the text."}), 400

    main_noun_obj = NounObject(main_noun_token.text)
    compound_nouns = find_compound_nouns(doc)
    associated_verbs = find_associated_verbs(doc, main_noun_token)
    associated_nouns = find_associated_nouns(doc, main_noun_token, compound_nouns)
    filtered_nouns = filter_nouns(associated_nouns, compound_nouns)

    for cn in compound_nouns:
        main_noun_obj.add_associated_noun(cn)
    for noun in filtered_nouns:
        main_noun_obj.add_associated_noun(noun)
    for verb in associated_verbs:
        main_noun_obj.add_associated_verb(verb)

    response = {
        "nouns": [main_noun_obj.to_dictionary()]
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

def spell_check_word(word):
    return spell.correction(word)

@app.route('/')
def hello_world():
    return 'Hello, World!'