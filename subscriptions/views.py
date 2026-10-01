from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, Subscription

def plan_list_view(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    return render(request, 'subscriptions/plan_list.html', {'plans': plans})

@login_required
def subscribe_view(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    if request.method == 'POST':
        # Simulate payment and create subscription
        # In reality, this would integrate with Stripe/PayPal
        end_date = timezone.now() + timedelta(days=plan.duration_days)
        
        # Deactivate existing subscriptions
        Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        Subscription.objects.create(
            user=request.user,
            plan=plan,
            end_date=end_date,
            is_active=True
        )
        return redirect('accounts:profile')
        
    return render(request, 'subscriptions/subscribe.html', {'plan': plan})
