from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as logIn, logout as logOut, authenticate
from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('accounts:register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already used')
                return redirect('accounts:register')

            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                logIn(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('pages:index')
                # user.save()
                # messages.success(request,'You are now registered in')
                # return redirect('accounts:login')

        else:
            messages.error(request, 'Password do not match')
            return redirect('accounts:register')
    return render(request, 'accounts/register.html')


def login(request):
    # Register user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            logIn(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def logout(request):
    logOut(request)
    messages.success(request, 'You are now logged out')
    return redirect('pages:index')


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)
