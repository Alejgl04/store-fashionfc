from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib import messages
from django.contrib.auth.models import User, auth

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

from .token import user_tokenizer_generate
from .forms import CreateUserForm, SignInForm, UpdateUserForm

# Create your views here.

def sign_up(request):
  
  form = CreateUserForm()
  
  if request.method == 'POST':
    
    form = CreateUserForm(request.POST)
    
    if form.is_valid():

      user = form.save()
      
      user.is_active = False
      
      user.save()
      
      # Email verification setup ( template )
      
      current_site = get_current_site(request)
      
      subject = 'Account verification email'
      
      message = render_to_string('account/registration/email-verification.html', {
        
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': user_tokenizer_generate.make_token(user),

      })
      
      user.email_user(subject=subject, message=message)
      
      return redirect('email-verification-sent')

  
  context = { 'form': form }
   
  return render(request, 'account/registration/sign-up.html', context)


def email_verification(request, uidb64, token):
  
  user_id = force_str(urlsafe_base64_decode(uidb64))
  
  user = User.objects.get(pk=user_id)

  if user and user_tokenizer_generate.check_token(user, token):
    
    user.is_active = True   

    user.save()
    
    return redirect('email-verification-success')
  
  else:
    
    return redirect('email-verification-failed')


def email_verification_sent(request):
  
  return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
  
  return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
  
  return render(request, 'account/registration/email-verification-failed.html')


def sign_in(request):
  
  form = SignInForm()
  
  if request.method == 'POST':
    
    form = SignInForm(request, data=request.POST)
    
    if form.is_valid():
      
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        auth.login( request, user )
        return redirect('dashboard')
  
  context = { 'form': form }
  return render(request, 'account/sign-in.html', context=context)


def sign_out(request):
  
  try:
    for key in list(request.session.keys()):
    
      if key == 'session_key':
      
        continue
      
      else:
      
        del request.session[key]
        
  except KeyError:
    pass
  # auth.logout(request)
  
  messages.success(request, 'Sign out success')
  
  return redirect('store')
  

@login_required(login_url='sign-in')
def dashboard(request):
  return render(request, 'account/dashboard.html')


@login_required(login_url='sign-in')
def profile_management(request):
  
  #Update email and username  
  user_form = UpdateUserForm(instance=request.user)
  
  if request.method == 'POST':
    user_form = UpdateUserForm(request.POST, instance=request.user)
    
    if user_form.is_valid():
      
      user_form.save()
      
      messages.info(request, 'Account updated')
  
      return redirect('dashboard')
    
  context = {'user_form': user_form}
  
  return render(request, 'account/profile-management.html', context)


@login_required(login_url='sign-in')
def delete_account(request):
  
  user = User.objects.get(id=request.user.id)
  
  if request.method == 'POST':
    
    user.delete()
    
    messages.error(request, 'Account deleted')

    return redirect('store')
    
  return render(request, 'account/delete-account.html')


#Shipping view

def manage_shipping(request):
  
  try:
    
    # account user with shipment information
    
    shipping = ShippingAddress.objects.get(user=request.user.id)
    
  except ShippingAddress.DoesNotExist:
    
    shipping = None
    
  
  form = ShippingForm(instance=shipping)
  
  if request.method == 'POST':
    
    form = ShippingForm(request.POST, instance=shipping)
    
    if form.is_valid():
      
      # Assign the user FK on the object
      shipping_user = form.save(commit=False)    
    
      # Adding the fk itself
      shipping_user.user = request.user
      
      shipping_user.save()

      return redirect('dashboard')
      
  context = { 'form': form }
  return render( request, 'account/manage-shipping.html', context )


@login_required(login_url='sign-in')
def track_orders(request):
  
  try:

    orders = OrderItem.objects.filter(user=request.user).order_by('-id')
    
    context = {'orders': orders}
    
    return render(request, 'account/track-orders.html', context)
  
  except:  
    return render(request, 'account/track-orders.html')