# GramaticalParser
Read me:

Project Setup README

Getting Started

This document outlines the steps taken to set up the backend for a grammatical parser project using Flask and SpaCy in a Python environment.

Prerequisites
  Python 3
  pip
  Virtual Environment (recommended)

Installation

Step 1: Set Up Virtual Environment (optional)

Open PowerShell or your preferred terminal.
Navigate to your project directory.
Create a virtual environment:
  Powershell Copy code: python -m venv venv
Activate the virtual environment:
  Powershell Copy code: .\venv\Scripts\Activate.ps1

After activation, you should see (venv) at the beginning of your prompt in the terminal.

Step 2: Install Flask
  Powershell Copy code: pip install Flask

Step 3: Install SpaCy
  Copy code: pip install spacy
  
Step 4: Download the English language model:
  Copy code: python -m spacy download en_core_web_sm
  
Step 5: Instasll NLTK
  Copy Code: pip install nltk

Step 6: Install spellchecker:
 Copy Code: pip install pyspellchecker

Final Step : Launch application

Run Flask Application:
Run the application by executing python app.py in your terminal. The app will start, and by default, it will be accessible at http://127.0.0.1:5000/ or http://localhost:5000/.



Notes: 

Join the Postman work space through this link: 

https://app.getpostman.com/join-team?invite_code=80cb87136c9ca80dbbf8d83e2bbfe497&target_code=ca01046166a0b4b3ad654f62bda7ed77


