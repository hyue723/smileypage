import string

def parse(input_s):
	return input_s.translate(None, string.punctuation).lower()

print parse("This, is a, let's say, test file.")