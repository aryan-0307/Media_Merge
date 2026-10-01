from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse, FileResponse, HttpResponseForbidden, Http404
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import os

from .models import MediaAsset, Category, AccessKey
from .forms import MediaAssetForm
from subscriptions.models import Subscription
from analytics.models import StreamingRecord, WatchHistory

def is_creator(user):
    return getattr(user, 'role', '') == 'CREATOR' or user.is_staff

def has_access_to_media(user, media):
    if user.is_staff or media.creator == user:
        return True
    if media.is_premium:
        # Check active subscription
        return Subscription.objects.filter(user=user, is_active=True, end_date__gt=timezone.now()).exists()
    return True

@login_required
def generate_access_token(request, pk):
    media = get_object_or_404(MediaAsset, pk=pk, publication_status='PUBLISHED')
    
    if not has_access_to_media(request.user, media):
        return JsonResponse({'error': 'Unauthorized or subscription required'}, status=403)
        
    # Generate token valid for 2 hours
    expires_at = timezone.now() + timedelta(hours=2)
    key = AccessKey.objects.create(
        user=request.user,
        media_asset=media,
        expires_at=expires_at
    )
    
    return JsonResponse({
        'token': str(key.token),
        'expires_at': expires_at.isoformat()
    })

def stream_media(request, token):
    key = get_object_or_404(AccessKey, token=token)
    
    if not key.is_valid():
        return HttpResponseForbidden("Access token expired")
        
    media = key.media_asset
    if media.publication_status != 'PUBLISHED':
        return HttpResponseForbidden("Media not published")
        
    # Record streaming start if not already recorded recently (debounce)
    # Simple logic: create record on first stream request
    recent_record = StreamingRecord.objects.filter(
        user=key.user, 
        media_asset=media,
        started_at__gte=timezone.now() - timedelta(minutes=5)
    ).exists()
    
    if not recent_record:
        StreamingRecord.objects.create(user=key.user, media_asset=media)
    
    if not media.media_file or not os.path.exists(media.media_file.path):
        raise Http404("Media file not found on server")
        
    # FileResponse handles Range requests automatically in Django
    return FileResponse(open(media.media_file.path, 'rb'), content_type='video/mp4')

@login_required
def update_progress(request, pk):
    if request.method == 'POST':
        progress = int(request.POST.get('progress', 0))
        media = get_object_or_404(MediaAsset, pk=pk)
        
        history, created = WatchHistory.objects.get_or_create(
            user=request.user, 
            media_asset=media
        )
        # Only update if progress is greater or within reasonable bounds
        if progress > history.progress_seconds:
            history.progress_seconds = progress
            history.save()
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid'}, status=400)

def home_view(request):
    featured_media = MediaAsset.objects.filter(publication_status='PUBLISHED').order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'catalog/home.html', {
        'featured_media': featured_media,
        'categories': categories
    })

def browse_view(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    media_list = MediaAsset.objects.filter(publication_status='PUBLISHED')
    
    if query:
        media_list = media_list.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_slug:
        media_list = media_list.filter(category__slug=category_slug)
        
    return render(request, 'catalog/browse.html', {
        'media_list': media_list,
        'query': query,
        'current_category': category_slug,
        'categories': Category.objects.all()
    })

def media_detail_view(request, pk):
    media = get_object_or_404(MediaAsset, pk=pk, publication_status='PUBLISHED')
    has_access = False
    if request.user.is_authenticated:
        has_access = has_access_to_media(request.user, media)
        
    return render(request, 'catalog/media_detail.html', {
        'media': media,
        'has_access': has_access
    })

from django.db.models import Count

@login_required
def creator_dashboard_view(request):
    if not is_creator(request.user):
        raise PermissionDenied
        
    my_media = MediaAsset.objects.filter(creator=request.user).order_by('-created_at')
    
    total_uploaded = my_media.count()
    published_count = my_media.filter(publication_status='PUBLISHED').count()
    
    # Total streams across all media owned by this creator
    total_streams = StreamingRecord.objects.filter(media_asset__creator=request.user).count()
    
    # Royalties
    from django.db.models import Sum
    from royalties.models import RoyaltyRecord
    total_earnings = RoyaltyRecord.objects.filter(creator=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    royalty_history = RoyaltyRecord.objects.filter(creator=request.user).select_related('media_asset').order_by('-calculated_at')[:10]
    
    # Media-wise streaming statistics for chart
    media_stats = my_media.annotate(
        stream_count=Count('streaming_records')
    ).values('title', 'stream_count')
    
    # Format data for Chart.js
    chart_labels = [m['title'] for m in media_stats]
    chart_data = [m['stream_count'] for m in media_stats]
    
    context = {
        'my_media': my_media,
        'total_uploaded': total_uploaded,
        'published_count': published_count,
        'total_streams': total_streams,
        'total_earnings': total_earnings,
        'royalty_history': royalty_history,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    
    return render(request, 'catalog/creator_dashboard.html', context)

@login_required
def media_upload_view(request):
    if not is_creator(request.user):
        raise PermissionDenied
        
    if request.method == 'POST':
        form = MediaAssetForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.creator = request.user
            media.save()
            return redirect('catalog:creator_dashboard')
    else:
        form = MediaAssetForm()
    return render(request, 'catalog/media_form.html', {'form': form, 'title': 'Upload Media'})

@login_required
def media_edit_view(request, pk):
    media = get_object_or_404(MediaAsset, pk=pk, creator=request.user)
    if request.method == 'POST':
        form = MediaAssetForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            return redirect('catalog:creator_dashboard')
    else:
        form = MediaAssetForm(instance=media)
    return render(request, 'catalog/media_form.html', {'form': form, 'title': 'Edit Media'})

@login_required
def media_delete_view(request, pk):
    media = get_object_or_404(MediaAsset, pk=pk, creator=request.user)
    if request.method == 'POST':
        media.delete()
        return redirect('catalog:creator_dashboard')
    return render(request, 'catalog/media_confirm_delete.html', {'media': media})

from django.core.paginator import Paginator
from .models import MovieDatasetRecord

def movie_database_list_view(request):
    queryset = MovieDatasetRecord.objects.all()
    
    # 1. Search
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(title__icontains=query)
        
    # 2. Filters
    language = request.GET.get('language', '').strip()
    if language:
        queryset = queryset.filter(language__iexact=language)
        
    genre = request.GET.get('genre', '').strip()
    if genre:
        queryset = queryset.filter(genre__icontains=genre)
        
    year = request.GET.get('year', '').strip()
    if year.isdigit():
        queryset = queryset.filter(release_year=int(year))
        
    # 3. Sorting
    sort = request.GET.get('sort', '')
    if sort == 'rating_desc':
        queryset = queryset.order_by('-rating', 'id')
    elif sort == 'rating_asc':
        queryset = queryset.order_by('rating', 'id')
    elif sort == 'year_desc':
        queryset = queryset.order_by('-release_year', 'id')
    elif sort == 'year_asc':
        queryset = queryset.order_by('release_year', 'id')
    elif sort == 'votes':
        queryset = queryset.order_by('-vote_count', 'id')
    else:
        # Default sort
        queryset = queryset.order_by('title', 'id')
        
    # Performance: use only necessary fields
    queryset = queryset.only('id', 'title', 'release_year', 'language', 'genre', 'runtime_minutes', 'rating', 'vote_count')
    
    # Pagination
    paginator = Paginator(queryset, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'q': query,
        'language': language,
        'genre': genre,
        'year': year,
        'sort': sort
    }
    return render(request, 'catalog/movie_database_list.html', context)

def movie_database_detail_view(request, pk):
    record = get_object_or_404(MovieDatasetRecord, pk=pk)
    return render(request, 'catalog/movie_database_detail.html', {'record': record})

