from django.shortcuts import render

from django.http import JsonResponse

from cart.cart import Cart
from . models import ShippingAddress, Order, OrderItem

# Create your views here.

def checkout( request ):

  if request.user.is_authenticated:
    
    try:     
      # authenticated users with shipping info
      shipping_address = ShippingAddress.objects.get(user=request.user.id)
      
      context = { 'shipping': shipping_address }
      
      return render( request, 'payment/checkout.html', context )

    except:
      # Authenticated users with no shipping information
      return render( request, 'payment/checkout.html' )

  return render( request, 'payment/checkout.html' )


def complete_order(request):
  
  print(request.POST)
  if request.POST.get('action') == 'post':
    name  = request.POST.get('name')
    email = request.POST.get('email')
    first_address  = request.POST.get('first_address')
    second_address = request.POST.get('second_address')
    city    = request.POST.get('city')
    state   = request.POST.get('state')
    zipcode = request.POST.get('zipcode')
    
    shipping_address = (first_address + "\n" + second_address + "\n" +
                        city + "\n" + state + "\n" + zipcode)
    
    # Shopping cart info
    cart = Cart(request)
    total_cost_items = cart.total()
    
    # Create order -> Account users with + without shipping information
    if request.user.is_authenticated:
      
      order = Order.objects.create(full_name = name, email = email, shipping_address = shipping_address, amount_paid = total_cost_items, user = request.user)
      
      order_id = order.pk
      
      for item in cart:
        
        OrderItem.objects.create(order_id=order_id, product = item['product'], quantity=item['qty'], price=item['price'], user=request.user)
    
    # Create order -> Guest users without and account 
    else:
      
      order = Order.objects.create(full_name = name, email = email, shipping_address = shipping_address, amount_paid = total_cost_items)
      
      order_id = order.pk
      
      for item in cart:
        
        OrderItem.objects.create(order_id=order_id, product = item['product'], quantity=item['qty'], price=item['price'])
    
    order_success = True
    response = JsonResponse({'success': order_success})
    return response
    
  
def payment_success( request ):
  
  # Clear shopping cart
  
  for key in list(request.session.keys()):
    
    if key == 'session_key':
      
      del request.session[key]
                   
  return render( request, 'payment/payment-success.html')


def payment_failed( request ):
  return render( request, 'payment/payment-failed.html')