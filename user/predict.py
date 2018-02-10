from .classify import *
import string

def parse(input_s):
    translator = str.maketrans('', '', string.punctuation)
    return input_s.translate(translator).lower()

def predict(input_text):
    input_text = parse(input_text)
    populateD()
    return classifyDoc(input_text)[:5]
