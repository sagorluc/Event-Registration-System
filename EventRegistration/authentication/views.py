from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from authentication.forms import RegistrationFrom, LoginForm
from django.contrib import messages

# ============================= USER REGISTRATION ==============================
def user_register(request):
    form = RegistrationFrom()
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'register.html', {'form': form})



# ============================= USER LOGIN ======================================
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = authenticate(username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Loged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'User not found')
            return redirect('login')             
    return render(request, 'login.html')


# ============================= USER LOGOUT =================================
@login_required
def log_out(request):
        
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully.')
    return redirect('login')
