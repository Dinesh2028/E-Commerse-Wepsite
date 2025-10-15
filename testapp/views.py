from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .form import UserRegistrationForm, UserLoginForm

def register(request):
    register_form = UserRegistrationForm()
    login_form = UserLoginForm()
    mode = 'register'  # Default mode

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('home')  # Assuming 'home' is the name of the home page URL
            else:
                messages.error(request, 'Please correct the errors below.')
                mode = 'register'
        elif 'login' in request.POST:
            login_form = UserLoginForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
                    mode = 'login'
            else:
                messages.error(request, 'Please correct the errors below.')
                mode = 'login'
        else:
            # Toggle mode
            mode = request.POST.get('mode', 'register')

    return render(request, 'shop/register.html', {
        'register_form': register_form,
        'login_form': login_form,
        'mode': mode
    })
