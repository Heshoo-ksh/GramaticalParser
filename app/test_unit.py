
from unittest.mock import Mock
import spacy
from app.views import (is_valid_english_word, find_associated_verbs, create_verb_phrase,
                         find_associated_nouns, find_compound_nouns, filter_nouns,
                         find_main_noun)

nlp = spacy.load("en_core_web_sm")
doc = nlp("As a project manager, I need a dashboard to track project progress.")
main_noun_token_with = find_main_noun(doc, "dashboard")  
main_noun_token_without = find_main_noun(doc, "")  

def test_is_valid_english_word_identifies_valid_word():
    assert is_valid_english_word("apple") is True

def test_is_valid_english_word_rejects_invalid_word():
    assert is_valid_english_word("asdfghjkl") is False

def test_find_associated_verbs_with_main_noun():
    result = find_associated_verbs(doc, main_noun_token_with)
    expected_verb_phrases_with = ["need dashboard",
                "track progress"] 
    assert set(result) == set(expected_verb_phrases_with)

def test_find_associated_verbs_without_main_noun():
    result = find_associated_verbs(doc, main_noun_token_without)
    expected_verb_phrases_without = ["need dashboard",
                "track progress"] 
    assert set(result) == set(expected_verb_phrases_without)

def test_create_verb_phrase_with_main_noun():
    verb_token = next(token for token in doc if token.text == "track")
    verb_lemma = verb_token.lemma_
    phrase_with = create_verb_phrase(verb_token, verb_lemma)
    assert phrase_with == "track progress"

def test_create_verb_phrase_without_main_noun():
    verb_token = next(token for token in doc if token.text == "track")
    verb_lemma = verb_token.lemma_
    phrase_without = create_verb_phrase(verb_token, verb_lemma)
    assert phrase_without == "track progress"

def test_find_compound_nouns_with_main_noun():
    result_with = find_compound_nouns(doc)
    expected_compounds_with = {"project manager","project progress"}
    assert set(result_with) == expected_compounds_with

def test_find_compound_nouns_without_main_noun():
    result_without = find_compound_nouns(doc)
    expected_compounds_without = {"project manager","project progress"}
    assert set(result_without) == expected_compounds_without

# Filter nouns
def test_filter_nouns_with_main_noun():
    individual_nouns = ["manager", "dashboard", "project"]
    compound_nouns_with = ["project manager"]
    expected_filtered_nouns_with = ["dashboard"]
    result_with = filter_nouns(individual_nouns, compound_nouns_with)
    assert set(result_with) == set(expected_filtered_nouns_with)

def test_filter_nouns_without_main_noun():
    individual_nouns = ["manager", "dashboard", "project"]
    compound_nouns_without = ["project manager"]
    expected_filtered_nouns_without = ["dashboard"]
    result_without = filter_nouns(individual_nouns, compound_nouns_without)
    assert set(result_without) == set(expected_filtered_nouns_without)