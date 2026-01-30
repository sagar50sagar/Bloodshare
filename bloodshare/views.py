from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, LoginForm, ProfileForm, DonationRequestForm
from .models import Profile, DonationRequest


def landing(request):
    """Public landing page"""
    # Mock stats for display
    stats = {
        'total_donors': 1250,
        'lives_saved': 3420,
        'active_requests': 45,
    }
    return render(request, 'bloodshare/landing.html', {'stats': stats})


def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to BloodShare.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'bloodshare/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Django uses username, but we're using email as username
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires on browser close
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'bloodshare/login.html', {'form': form})


@login_required
def dashboard(request):
    """Authenticated user dashboard"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get user's donation requests
    user_requests = DonationRequest.objects.filter(requester=request.user)[:10]
    
    # Get all active donation requests (for browsing)
    all_requests = DonationRequest.objects.filter(status='pending').exclude(requester=request.user)[:20]
    
    if request.method == 'POST':
        # Handle donation request creation
        request_form = DonationRequestForm(request.POST)
        if request_form.is_valid():
            donation_request = request_form.save(commit=False)
            donation_request.requester = request.user
            donation_request.save()
            messages.success(request, 'Donation request created successfully!')
            return redirect('dashboard')
    else:
        request_form = DonationRequestForm()
    
    # Profile form for editing
    profile_form = ProfileForm(instance=profile, user=request.user)
    
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'request_form': request_form,
        'user_requests': user_requests,
        'all_requests': all_requests,
    }
    return render(request, 'bloodshare/dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_availability(request):
    """API endpoint to toggle donor availability"""
    try:
        profile = Profile.objects.get(user=request.user)
        profile.is_available = not profile.is_available
        profile.save()
        return JsonResponse({
            'success': True,
            'is_available': profile.is_available,
            'message': 'Availability updated successfully'
        })
    except Profile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)


@login_required
def update_profile(request):
    """Update user profile"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    
    return render(request, 'bloodshare/profile_edit.html', {'form': form, 'profile': profile})
