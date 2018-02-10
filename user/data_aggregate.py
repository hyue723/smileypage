# aggregate data based on location & range
# select at most 5 keywords of the highest frequencies
from .models import Event, Profile, User, Friend, FriendshipRequest
from urllib2 import urlopen
import json, string
import parse

API_KEY = "AIzaSyCBsS-L1dORWZQM45rIVd-9wjCqzbxc5jI"

def standardize(address):
	return string.replace(' '.join(address.split()), ' ', '+')

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.PI / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000

def getgeo(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    address = standardize(address)
    url += "address=%s&key=%s" % (address, API_KEY)
    v = urlopen(url).read()
    j = json.loads(v)
    geo = j['results'][0]['geometry']['location']
    return (geo['lat'], geo['lng'])

def distance(lat, lng, lat1, lng1):
	return measure(lat, lng, lat1, lng1)

def aggregateDataWithinRange(location, radius):
	tmp = []
	lat, lng = getgeo(location)
	for Event in Event.objects.all():
		symptom = "none"
		#convert location to [lat, lon]
		lat1, lng2 = getgeo(event.location)
		symptoms = parse.parse(event.symptoms)
		prediction = event.prediction
		for symptom in symptoms: 
			if symptom in prediction: 
				symptom = symptom
				break
		if distance(lat, lng, lat1, lng1) <= radius:
			tmp.append(symptom + ' ' + str(lat1) + ' ' + str(lng1))
	return tmp

def aggregateUserData(request):
	query = request.GET.get("q")
	if not query: return []
	user = Profile.objects.get(user=request.user)
	events = Event.objects.filter(user=request.user).order_by('-date')
	location = user.location
	radius = user.radius
	context = dict()
	context['location'] = aggregateDataWithinRange(location, radius)
	return render(request, 'user/visualize.html', context)