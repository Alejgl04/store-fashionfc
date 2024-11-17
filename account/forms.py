
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.widgets import PasswordInput, TextInput

from django import forms

class CreateUserForm(UserCreationForm):
  
  def __init__(self, *args, **kwargs):
    super(CreateUserForm, self).__init__(*args, **kwargs)
    
    self.fields['email'].required = True
    self.fields['password1'].required = True
    self.fields['password2'].required = True
    
  class Meta:
    
    model = User
    fields = ['username', 'email', 'password1', 'password2']
      
    def clean_email(self):
      email = self.cleaned_data.get('email')
      
      if User.objects.filter(email=email).exists():
        
        raise forms.ValidationError('Email already exist')
      
      if len(email) >= 350:
        
        raise forms.ValidationError('Email too long')
               
      return email


class SignInForm(AuthenticationForm):
  
  username = forms.CharField(widget=TextInput(), strip=False)
  password = forms.CharField(widget=PasswordInput())

class UpdateUserForm(forms.ModelForm):
  password = None
  
  class Meta:
    
    model = User
    fields = ['username', 'email']
    exclude = ['password1', 'password1']
    
  def __init__(self, *args, **kwargs):
    super(UpdateUserForm, self).__init__(*args, **kwargs)
  
    self.fields['email'].required = True
    
  def clean_email(self):
    email = self.cleaned_data.get('email')
    
    if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
      
      raise forms.ValidationError('Email already exist')
    
    if len(email) >= 350:
      
      raise forms.ValidationError('Email too long')
              
    return email