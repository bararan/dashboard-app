from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(req):
    err_msg = None
    form = AuthenticationForm()
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                if req.GET.get('next'): # If redirecting to a specific page post-login. This is automatically added to the request if user tries to access a specific page (e.g. /reports) before logging in.
                    return redirect(req.GET.get('next'))
                return redirect('sales:home')
    err_msg = 'Something went wrong. Please try again.'
    context = {
        'form': form,
        'error_message': err_msg,
    }
    return render(req, 'auth/login.html', context=context)

def logout_view(req):
    logout(req)
    return redirect('login')
