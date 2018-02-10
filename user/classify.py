import math, re, os

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))
	
FILEPATH = "result.txt"
ALPHA = 0.1
V = 500

d = dict()


def getDiseases():
	__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
	f = open(os.path.join(__location__, 'diseases.txt'), 'r')
	diseases = []
	line = f.readline()
	while line:
		line = line.strip()
		diseases.append(line)
		line = f.readline()

	return diseases

classification = getDiseases()

def tokenizeDoc(cur_doc):
	return re.findall('\\w+', cur_doc)

def populateD(): #Note: write count result to stdout
	f = f = open(os.path.join(__location__, 'result.txt'), 'r')

	line = f.readline()
	while line:
		l = line.split('\t')
		key, v = l[0], l[1]
		d[key] = int(v)
		line = f.readline()

	f.close()
	
def YPrior(y):
	# calculates prior (in respect to y) with Laplace smoothing
	# p(Y=y) = Y=y count + ALPHA / Y= * count + ALPHA
	k = 'Y=' + y
	key_l = len(k)
	key_count = 0
	total_count = 0
	#msgs.seek(0) #start search from the start of the message file
	
	#lookup number of occurrences of key in accumulated msgs
	for key in d:
		if key == k: 
			key_count = d[key]
		elif key == 'Y=*':
			total_count =  d[key]
		if (key_count != 0 and total_count != 0): break
	return (key_count + ALPHA) / (total_count + ALPHA * len(classification))

def WGivenY(w, y):
	# p(W=w|Y=y) = W=w & Y=y count + ALPHA / Y=y count + ALPHA * dim
	
	key_y = 'Y=' + y + ',W=*'
	key_w = 'Y=' + y + ',W=' + w
	WCount = 0
	YCount = 0
	V = len(d)
	#msgs.seek(0) #start search from the start of the message file

	#lookup number of occurrences of key in accumulated msgs
	for key in d:
		if key == key_w:
			WCount = d[key]
		elif key == key_y:
			YCount = d[key]
		if (WCount != 0 and YCount != 0): break

	return (WCount + ALPHA) / (YCount + ALPHA * V)

def tokenizeDoc(cur_doc):
	return re.findall('\\w+', cur_doc)

def classifyDoc(cur_doc):
	# returns (actual classes, best class, max log probability) tuple

	#initialize counters & log probabilities
	prob_log = [0] * len(classification)
	#classification = ['CCAT', 'ECAT', 'GCAT', 'MCAT']

	tokenized = tokenizeDoc(cur_doc)
	N = len(tokenized)

	#calculate log probability for each y to find the best class
	index = 0

	for y in classification:
		log_prob = 0	
		prior = YPrior(y)
		#calculate evidence
		for key in tokenized:
			log_prob += math.log(WGivenY(key, y))

		prob_log[index] = log_prob + math.log(prior)
		index += 1

	best_prob = max(prob_log)

	result = sorted(zip(classification, prob_log), key=lambda tup: tup[1], reverse=True)

	#print "DEBUGGING ONLY: ", prob_log
	return result