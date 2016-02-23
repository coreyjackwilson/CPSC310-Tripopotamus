from django import forms
from models import Member, Trip
from django.contrib.auth.hashers import check_password

class AccountCreationForm(forms.ModelForm):
    username = forms.CharField(label='Your username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Member
        app_label = 'tripapotamus'
        fields = ('username', 'password',)
        
    def save(self, commit=True):
        return super(AccountCreationForm, self).save(commit=commit)
    
class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Your username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Member
        app_label = 'tripapotamus'
        fields=('username', 'password',)
        
    def save(self, commit=True):
        return super(LoginForm, self).save(commit=commit)
    
class TripForm(forms.ModelForm):
    firstPoint = forms.CharField(max_length=75)
    lastPoint = forms.CharField(max_length=75)
    moneySaved = forms.DecimalField(max_digits=10,decimal_places=2)
    distanceTravelled = forms.DecimalField(max_digits=20,decimal_places=4)
    
    class Meta:
        model = Trip
        app_label = 'tripapotamus'
        fields = '__all__'

    