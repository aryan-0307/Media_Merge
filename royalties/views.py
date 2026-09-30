from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .services import calculate_royalties

def is_admin(user):
    return user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def process_royalties_view(request):
    if request.method == 'POST':
        result = calculate_royalties()
        if result['records_created'] > 0:
            messages.success(request, f"Processed {result['records_created']} royalty records totaling ${result['total_payout']}.")
        else:
            messages.info(request, "No new eligible streams to process.")
    return redirect('analytics:admin_dashboard')
