from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog:home')
    else:
        form = AuthenticationForm()
        # Add CSS classes
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('catalog:home')

from subscriptions.models import Subscription
from analytics.models import WatchHistory
from django.utils import timezone

@login_required
def profile_view(request):
    active_subscription = Subscription.objects.filter(
        user=request.user, 
        is_active=True, 
        end_date__gt=timezone.now()
    ).first()
    
    watch_history = WatchHistory.objects.filter(user=request.user).select_related('media_asset').order_by('-last_watched')[:10]
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'subscription': active_subscription,
        'watch_history': watch_history,
    })
