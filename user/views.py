from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View
from .forms import UserForm, ProfileForm, EventForm, FriendshipRequestForm
from django.template import loader
from .models import Event, Profile, User, Friend, FriendshipRequest
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.db.models import Q


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
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
                return render(request, 'user/login.html', {'error_message': 
                           "The user account is not active"})
    if login_initial == False:
        return render(request, 'user/login.html', {'error_message': 
        "Either the username or the password is incorrect. Please try again."})
    return render(request, 'user/login.html')


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
            events = events.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events = events.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
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
            events =events_mine.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events =events_mine.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events =events_mine.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events =events_all.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events =events_all.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
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
            events =events_all.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query)  |
                                   Q(date__icontains=query)  | 
                                   Q(start_time__icontains=query)| 
                                   Q(end_time__icontains=query)|
                                   Q(location__icontains=query)|
                                   Q(kind__icontains=query)|
                            Q(user__username__icontains=query)).distinct()
            events=events.order_by('-date')
        context = {'events':events, 'user':user}
        return render(request, 'user/all_events.html', context)

def request_detail(request, message_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        message = get_object_or_404(FriendshipRequest, id=message_id)
        message.viewed=True
        message.save()
        context = {'user':user, "message":message}
        return render (request, 'user/request_detail.html', context) 

def request_detail_sent(request, message_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        message = get_object_or_404(FriendshipRequest, id=message_id)
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
        friendships = Friend.objects.filter(from_user=user)
        message = FriendshipRequest.objects.filter(Q(from_user=user, 
            to_user = other_user)|
                        Q(to_user=user, from_user = other_user)).distinct()
        friended = friendships.filter(to_user=other_user)
        context={'user':user, 'other_user':other_user, 'profiles':profiles, 
        'friended':friended, 'message':message}
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
                                   Q(interest__icontains=query)  |
                                   Q(status_in_cmu__icontains=query)  | 
                                   Q(user__email__icontains=query)| 
                        Q(studying_fields__icontains=query)).distinct()

        context = {'user':user, 'users':users, 'profiles':profiles}
        return render(request, 'user/friends_search.html', context)



def friends_events_current(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        friends = profile.friends.all()
        events = set()
        for friend in friends:
            events=events.union(Event.objects.filter(user=friend, 
                date=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def friends_events_past(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        friends = profile.friends.all()
        events = set()
        for friend in friends:
            events=events.union(Event.objects.filter(user=friend, 
                date__lt=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def friends_events_future(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user = request.user
        profile =get_object_or_404(Profile, user=user)
        friends = profile.friends.all()
        events = set()
        for friend in friends:
            events=events.union(Event.objects.filter(user=friend,
                date__gt=datetime.date.today()))
        context = {'events':events, 'user':user}
        return render(request, 'user/friends_events.html', context)

def send_request(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        to_user = get_object_or_404(User, pk = user_id)
        form = FriendshipRequestForm(request.POST or None)
        from_user = request.user
        if form.is_valid():
            friendship = form.save(commit = False)
            friendship.from_user = from_user
            friendship.to_user= to_user
            friendship.save()
            return HttpResponseRedirect(reverse('user:user_detail', 
                args = (to_user.id,)))
        context = {'form':form, 'to_user':to_user, 'from_user':from_user}
    return render(request, 'user/FriendshipRequest.html', context)


def display_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:login'))
    else:
        user=request.user
        received=FriendshipRequest.objects.filter(to_user=user).order_by(
            '-created')
        sent=FriendshipRequest.objects.filter(from_user=user).order_by(
            '-created')
        context = {'user':user, 'received':received, 'sent':sent}
        return render(request, 'user/display_request.html', context)



def display_friends(request):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        friends = profile.friends.all()
        query = request.GET.get("q")
        requests = FriendshipRequest.objects.filter(to_user=user)
        if query:
            friends = friends.filter(Q(username__icontains=query) |
                                   Q(email__icontains=query)).distinct()
        context = {'friends':friends, 'requests':requests, 'user':user}
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
        message = get_object_or_404(FriendshipRequest, pk = message_id)
        message.viewed = True
        message.accepted = True
        message.save()
        relation = Friend()
        relation.to_user = message.from_user
        relation.from_user = message.to_user
        relation.save()
        relation_reverse = Friend()
        relation_reverse.to_user = message.to_user
        relation_reverse.from_user = message.from_user
        relation_reverse.save()
        user_profile = get_object_or_404(Profile, user = user)
        user_profile.friends.add(message.from_user)
        user_profile.save()
        other_profile = get_object_or_404(Profile, user=message.from_user)
        other_profile.friends.add(user)
        other_profile.save()
        context = {'user':user, "message": message}
        return render(request, 'user/request_detail.html', context)

def reject_friendship(request, message_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        user = request.user
        message = get_object_or_404(FriendshipRequest, pk = message_id)
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
        messages = FriendshipRequest.objects.filter(id=friend_request_id)
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
        message=FriendshipRequest.objects.filter(from_user=user,to_user=friend)
        message.delete()
        message_reverse = FriendshipRequest.objects.filter(to_user = user,
            from_user=friend)
        message_reverse.delete()
        user_profile=get_object_or_404(Profile, user=user)
        user_profile.friends.remove(friend)
        user_profile.save()
        friend_profile=get_object_or_404(Profile, user=friend)
        friend_profile.friends.remove(user)
        friend_profile.save()
        return HttpResponseRedirect(reverse("user:display_friends"))




