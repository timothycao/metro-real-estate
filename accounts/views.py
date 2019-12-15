from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from inquiries.models import Inquiry

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        # Check email
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is already used')
          return redirect('register')
        else:
          # Create account
          user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
          # Redirect to login
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    # Get form values
    username = request.POST['username']
    password = request.POST['password']
    # Authenticate values
    user = auth.authenticate(username=username, password=password)

    # Check if user exists
    if user is not None:
      auth.login(request, user)
      # Redirect to dashboard
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('index')

def dashboard(request):
  user_inquiries = Inquiry.objects.order_by('-inquiry_date').filter(user_id=request.user.id)

  context = {
    'inquiries': user_inquiries
  }
  return render(request, 'accounts/dashboard.html', context)
