from .classify import *

def predict(input_text):
	classify.populateD()
	return classify.classifyDoc(input_text)[:5]
