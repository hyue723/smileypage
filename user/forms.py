from django.contrib.auth.models import User
from django import forms
from .models import Profile, Event, HelpRequest
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
        fields =['radius', 'profile_photo', 'location',
        'status']
        labels = {
            'radius':_('Radius of Interest'),
            'profile_photo':_('Profile Photo'),
            'status':_('Your Status'),
            'location':_('Your Location'),
            # 'facebook_page':_('Your Facebook Profile Page URL (optional)'),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['symptoms', 'date', 'location', 'prediction']
        widgets = {
            'date': SelectDateWidget(),
            # 'end_time': forms.TimeInput(format='%H:%M'),
            # 'start_time': forms.TimeInput(format='%H:%M'),
        }
        labels = {
            'symptoms':_('Description'),
            'date':_("Date"),
            'location':_('Location'),
            }


class HelpRequestForm(forms.ModelForm):

    class Meta:
        model = HelpRequest
        fields = ['message']