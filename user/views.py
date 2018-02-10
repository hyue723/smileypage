from .predict import *
from .imageClassify import *

from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View
from .forms import UserForm, ProfileForm, EventForm, HelpRequestForm
from django.template import loader
from .models import Event, Profile, User, Connection, HelpRequest
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.db.models import Q


# aggregate data based on location & range
# select at most 5 keywords of the highest frequencies
from urllib.request import urlopen
import json, string



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # email = form.cleaned_data['email']
        user.set_password(password)
        user.save()
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user:login'))
    context = {'form':form,}
    return render(request, 'user/registration_form.html', context)


def login_user(request):
    login_initial = True
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        login_initial = False
        if user is not None:
            if user.is_active:
                login(request, user)
                profiles = Profile.objects.filter(user=request.user)
                context = {'user':user, 'profiles':profiles}
                if not profiles:
                    return HttpResponseRedirect(reverse('user:create_profile'))
                else:
                    return HttpResponseRedirect(reverse('user:profile'))
            else:
                return render(request, 'user/login_med.html', {'error_message': 
                           "The user account is not active"})
    if login_initial == False:
        return render(request, 'user/login_med.html', {'error_message': 
        "Either the username or the password is incorrect. Please try again."})
    return render(request, 'user/login_med.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def display_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))

    else:
        user = request.user
        profiles = Profile.objects.filter(user=request.user)
        events = Event.objects.filter(user=request.user).order_by('-date')
        query = request.GET.get("q")
        if query:
            events = events.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)).distinct()
        return render(request, 'user/profile.html', {'profiles':profiles, 
            'user':user, 'events':events})


def create_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            profile.save()
            profiles = Profile.objects.filter(user=request.user)
            return HttpResponseRedirect(reverse('user:profile'))
        context = {'form': form}
    return  render(request, 'user/create_profile.html', context)


def all_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        events = Event.objects.all().order_by('-date')
        query = request.GET.get("q")
        if query:
            events = events.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        query2 = request.GET.get("l")
        if query2:
            render(request, '')
        context = {"events":events, 'user':user}
    return render(request, 'user/all_events.html', context)



def create_event(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        form = EventForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit = False)
            event.user = request.user
            symptoms_photo = event.photo
            prediction = predict(event.symptoms)
            result = ""
            # create a table later on
            disease, p = prediction[0]
            prob = (math.e**p) *  100
            result = "Disease is " + disease + "with %.2f percent probability\n"%(abs(p))
            # if symptoms_photo != '/static/images/bg-01.jpg':
            #     test = analyze_image(symptoms_photo)
            #     if test:
            #         result = result + "Your skin-disease test is Positive."
            #     else:
            #         result = result + "Your skin-disease test is Negative."
            # else:
            #     result = "aha"
            event.prediction = result
            event.save()
            events = Event.objects.filter(user=request.user)
            return HttpResponseRedirect(reverse('user:profile'))
        context = {'form': form}
    return render(request, 'user/create_event.html', context)


def delete_event(request, event_id):
    event = Event.objects.get(pk = event_id)
    event.delete()
    return HttpResponseRedirect(reverse('user:profile'))


def edit_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        profile = get_object_or_404(Profile, user=user)
        form=ProfileForm(request.POST or None, instance =profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
        context = {'form':form, 'user':user}
        return render(request, 'user/edit_profile.html', context)

def edit_event(request, event_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        event = get_object_or_404(Event, id=event_id)
        form=EventForm(request.POST or None, instance =event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:event_detail', 
                args = (event.id,)))
        context = {'form':form, 'user':user}
        return render(request, 'user/create_event.html', context)



def event_detail(request, event_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        event = get_object_or_404(Event, pk = event_id)
        context = {'event':event, 'user':user}
        return render(request, 'user/event_detail.html', context)

def myevents_current(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        profiles = Profile.objects.filter(user=user)
        query = request.GET.get("q")
        events_mine = Event.objects.filter(user=user).order_by('-date')
        events=events_mine.filter(date=datetime.date.today()).order_by('-date')
        if query:
            events =events_mine.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user, 'profiles':profiles}
        return render(request, 'user/profile.html', context)

def myevents_past(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        profiles = Profile.objects.filter(user=user)
        query = request.GET.get("q")
        events_mine = Event.objects.filter(user=user).order_by('-date')
        events=events_mine.filter(date__lt=datetime.date.today()
            ).order_by('-date')
        if query:
            events =events_mine.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user, 'profiles':profiles}
        return render(request, 'user/profile.html', context)

def myevents_future(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        profiles = Profile.objects.filter(user=user)
        query = request.GET.get("q")
        events_mine = Event.objects.filter(user=user).order_by('-date')
        events=events_mine.filter(date__gt=datetime.date.today()
            ).order_by('-date')
        if query:
            events =events_mine.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user, 'profiles':profiles}
        return render(request, 'user/profile.html', context)

def allevents_current(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        query = request.GET.get("q")
        events_all = Event.objects.all().order_by('-date')
        events=events_all.filter(date=datetime.date.today()).order_by('-date')
        if query:
            events =events_all.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user}
        return render(request, 'user/all_events.html', context)

def allevents_past(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        events_all = Event.objects.all().order_by('-date')
        events=events_all.filter(date__lt=datetime.date.today()
            ).order_by('-date')
        query = request.GET.get("q")
        if query:
            events =events_all.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user}
        return render(request, 'user/all_events.html', context)

def allevents_future(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        events_all = Event.objects.all().order_by('-date')
        events=events_all.filter(date__gt=datetime.date.today()
            ).order_by('-date')
        query = request.GET.get("q")
        if query:
            events =events_all.filter(Q(symptoms__icontains=query) |
                                   Q(date__icontains=query)  | 
                                   Q(prediction__icontains=query)|
                                   Q(location__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user}
        return render(request, 'user/all_events.html', context)

def request_detail(request, message_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        message = get_object_or_404(HelpRequest, id=message_id)
        message.viewed=True
        message.save()
        context = {'user':user, "message":message}
        return render (request, 'user/request_detail.html', context) 

def request_detail_sent(request, message_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        message = get_object_or_404(HelpRequest, id=message_id)
        context = {'user':user, "message":message}
        return render (request, 'user/request_detail_sent.html', context) 

def otherevent_detail(request, event_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        event = get_object_or_404(Event, pk = event_id)
        context = {'event':event, 'user':user}
        return render(request, 'user/otherevent_detail.html', context)



def user_detail(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        other_user=get_object_or_404(User, id=user_id)
        profiles = Profile.objects.filter(user=other_user)
        connections = Connection.objects.filter(from_user=user)
        message = HelpRequest.objects.filter(Q(from_user=user, 
            to_user = other_user)|
                        Q(to_user=user, from_user = other_user)).distinct()
        connected = connections.filter(to_user=other_user)
        context={'user':user, 'other_user':other_user, 'profiles':profiles, 
        'connected':connected, 'message':message}
        return render(request, 'user/user_detail.html', context)

def friends_search(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        users=User.objects.all()
        profiles=Profile.objects.exclude(user=user)
        query = request.GET.get("q")
        if query:
            profiles = profiles.filter(Q(user__username__icontains=query) |
                                   Q(location__icontains=query)  |
                                   Q(status__icontains=query)  | 
                                   Q(user__email__icontains=query)).distinct()

        context = {'user':user, 'users':users, 'profiles':profiles}
        return render(request, 'user/friends_search.html', context)



def friends_events_current(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        connections = profile.connections.all()
        events = set()
        for connection in connections:
            events=events.union(Event.objects.filter(user=connection, 
                date=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def friends_events_past(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        connections = profile.connections.all()
        events = set()
        for connection in connections:
            events=events.union(Event.objects.filter(user=connection, 
                date__lt=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def friends_events_future(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        connections = profile.connections.all()
        events = set()
        for connection in connections:
            events=events.union(Event.objects.filter(user=connection,
                date__gt=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def send_request(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        to_user = get_object_or_404(User, pk = user_id)
        form = HelpRequestForm(request.POST or None)
        from_user = request.user
        if form.is_valid():
            connection = form.save(commit = False)
            connection.from_user = from_user
            connection.to_user= to_user
            connection.save()
            return HttpResponseRedirect(reverse('user:user_detail', 
                args = (to_user.id,)))
        context = {'form':form, 'to_user':to_user, 'from_user':from_user}
    return render(request, 'user/FriendshipRequest.html', context)


def display_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        received=HelpRequest.objects.filter(to_user=user).order_by(
            '-created')
        sent=HelpRequest.objects.filter(from_user=user).order_by(
            '-created')
        context = {'user':user, 'received':received, 'sent':sent}
        return render(request, 'user/display_request.html', context)



def display_friends(request):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        connections = profile.connections.all()
        query = request.GET.get("q")
        requests = HelpRequest.objects.filter(to_user=user)
        if query:
            connections = connections.filter(Q(username__icontains=query) |
                                   Q(email__icontains=query)).distinct()
        context = {'connections':connections, 'requests':requests, 'user':user}
        return render(request, 'user/friends.html', context)


def friends_events(request):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        friends = profile.friends.all()
        events = set()
        for friend in friends:
            events=events.union(Event.objects.filter(user=friend))
        query = request.GET.get("q")
        if query:
            events = events.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(user__username__icontains=query)|
                                   Q(user__email__icontains=query)|
                                   Q(kind__icontains=query)|
                                   Q(location__icontains=query)).distinct()
        context={'user':user, 'events':events}

        return render(request, 'user/friends_events.html', context)





def accept_friendship(request, message_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        message = get_object_or_404(HelpRequest, pk = message_id)
        message.viewed = True
        message.accepted = True
        message.save()
        relation = Connection()
        relation.to_user = message.from_user
        relation.from_user = message.to_user
        relation.save()
        relation_reverse = Connection()
        relation_reverse.to_user = message.to_user
        relation_reverse.from_user = message.from_user
        relation_reverse.save()
        user_profile = get_object_or_404(Profile, user = user)
        user_profile.connections.add(message.from_user)
        user_profile.save()
        other_profile = get_object_or_404(Profile, user=message.from_user)
        other_profile.connections.add(user)
        other_profile.save()
        context = {'user':user, "message": message}
        return render(request, 'user/request_detail.html', context)

def reject_friendship(request, message_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        message = get_object_or_404(HelpRequest, pk = message_id)
        message.viewed = True
        message.rejected = True
        message.save()
        context = {'user':user, "message": message}
        return render(request, 'user/request_detail.html', context)

def friend_request_detail(request, friend_request_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        messages = HelpRequest.objects.filter(id=friend_request_id)
        context = {'user':user, "messages": messages}
        return render(request, "user/request_message.html", context)


def delete_friend(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        friend = get_object_or_404(User, id=user_id)
        relation = Friend.objects.filter(from_user=user, to_user=friend)
        relation.delete()
        relation_reverse = Friend.objects.filter(to_user=user,from_user=friend)
        relation_reverse.delete()
        message=HelpRequest.objects.filter(from_user=user,to_user=friend)
        message.delete()
        message_reverse = HelpRequest.objects.filter(to_user = user,
            from_user=friend)
        message_reverse.delete()
        user_profile=get_object_or_404(Profile, user=user)
        user_profile.friends.remove(friend)
        user_profile.save()
        friend_profile=get_object_or_404(Profile, user=friend)
        friend_profile.friends.remove(user)
        friend_profile.save()
        return HttpResponseRedirect(reverse("user:display_friends"))



def parse(input_s):
    translator = str.maketrans('', '', string.punctuation)
    return input_s.translate(translator).lower()


API_KEY = "AIzaSyCBsS-L1dORWZQM45rIVd-9wjCqzbxc5jI"

def standardize(address):
    return (' '.join(address.split())).replace(' ', '+')

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000

def getgeo(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    address = standardize(address)
    url += "address=%s&key=%s" % (address, API_KEY)
    v = urlopen(url).read()
    j = json.loads(v.decode("ascii"))
    geo = j['results'][0]['geometry']['location']
    return (geo['lat'], geo['lng'])

def distance(lat, lng, lat1, lng1):
    return measure(lat, lng, lat1, lng1)

def aggregateDataWithinRange(location, radius):
    tmp = []
    lat, lng = getgeo(location)
    for event in Event.objects.all():
        symptom = "none"
        #convert location to [lat, lon]
        lat1, lng1 = getgeo(event.location)
        symptoms = parse(event.symptoms)
        prediction = event.prediction
        for symptom in symptoms: 
            if prediction != None and symptom in prediction: 
                symptom = symptom
                break
        if distance(lat, lng, lat1, lng1) <= radius:
            tmp.append(symptom + ' ' + str(lat1) + ' ' + str(lng1))
    return tmp

def aggregateUserData(request):
    # query = request.GET.get("l")
    # # if not query: return []
    user = Profile.objects.get(user=request.user)
    events = Event.objects.filter(user=request.user).order_by('-date')
    location = user.location
    radius = user.radius
    context = dict()
    context['location'] = aggregateDataWithinRange(location, radius)
    return render(request, 'user/visualize.html', context)