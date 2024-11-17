
from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
  
  class Meta:
    
    model = ShippingAddress
    
    fields = ['full_name', 'email', 'first_address', 'second_address', 'city', 'state', 'zipcode']
    
    exclude = ['user',]
    
    