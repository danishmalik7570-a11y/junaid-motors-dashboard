from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import StaffProfile
from .forms import StaffForm


def staff_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'staff/login.html')


def staff_logout(request):
    logout(request)
    return redirect('staff_login')


@login_required
def staff_list(request):
    staff = StaffProfile.objects.select_related('user').all()
    return render(request, 'staff/list.html', {'staff': staff})


@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'A user with this username already exists.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                )
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'Staff member added successfully.')
                return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/form.html', {'form': form, 'title': 'Add Staff'})
