from django.contrib.auth.models import User
from django import forms
from .models import Profile, Event, FriendshipRequest
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.forms import DateTimeInput, Textarea, TimeInput
from django.utils.translation import ugettext_lazy as _


class UserForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta: #information about Users
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields =['interest', 'profile_photo', 
        'status_in_cmu', 'studying_fields', 'facebook_page']
        labels = {
            'interest':_('Interested in'),
            'profile_photo':_('Profile Photo'),
            'status_in_cmu':_('Your Status in CMU'),
            'studying_fields':_('Your Studying Fields'),
            'facebook_page':_('Your Facebook Profile Page URL (optional)'),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'kind','description',
        'start_time', 'end_time', 'date', 'location', 'event_photo']
        widgets = {
            'date': SelectDateWidget(),
            'end_time': forms.TimeInput(format='%H:%M'),
            'start_time': forms.TimeInput(format='%H:%M'),
        }
        labels = {
            'end_time':_('End Time'),
            'start_time':_('Start Time'),
            'name':_('Event Name'),
            'description':_('Description'),
            'date':_("Date"),
            'location':_('Location'),
            'kind':_('Event Type'),
            'event_photo':_('Event Photo'),
            }


class FriendshipRequestForm(forms.ModelForm):

    class Meta:
        model = FriendshipRequest
        fields = ['message']