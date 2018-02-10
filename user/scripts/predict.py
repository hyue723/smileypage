import classify

def predict(input_text):
	classify.populateD()
	return classify.classifyDoc(input_text)[:5]

print predict('cough fever headache')