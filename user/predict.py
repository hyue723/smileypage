from .classify import *
import string

def parse(input_s):
    return input_s.translate(None, string.punctuation).lower()

def predict(input_text):
    input_text = parse(input_text)
    classify.populateD()
    return classify.classifyDoc(input_text)[:5]
