from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry

def inquiry(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']

    # Check if user has already made an inquiry for the listing
    if request.user.is_authenticated:
      user_id = request.user.id
      has_inquired = Inquiry.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_inquired:
        messages.error(request, 'You have already made an inquiry for this listing.')
        return redirect('/listings/' + listing_id)

    inquiry = Inquiry(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)

    inquiry.save()

    messages.success(request, 'Your request has been submitted. A realtor will get back to you shortly.')
    return redirect('/listings/' + listing_id)
