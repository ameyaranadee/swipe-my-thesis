from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from .models import UserProfile, ResearchInterest, UserLikedPapers
from django.contrib.auth.models import User
import random



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing_page')  # Redirect to landing page after login
    # If authentication failed (e.g. Guest user login)
            else:
                # Check if the username is 'Guest'
                if username == 'Guest':
                    user, created = User.objects.get_or_create(username='Guest')
                    # Optionally set a random password if you want to allow guest users to log in
                    if created:
                        user.set_password('guestpassword123')  # Set a default password
                        user.save()
                    login(request, user)
                    return redirect('landing_page')  # Redirect to landing page
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'app/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Ensure form handles file uploads
        if form.is_valid():
            # Save the User (this will create the User instance)
            user = form.save()
            login(request, user)
            # # Create and save UserProfile with additional user information
            # user_profile = UserProfile(
            #     user=user,
            #     profile_picture=form.cleaned_data.get('profile_picture'),
            #     university=form.cleaned_data.get('university'),
            #     major=form.cleaned_data.get('major'),
            #     courses=form.cleaned_data.get('courses')
            # )
            # user_profile.save()

            # Handle research interests
            # research_interests = form.cleaned_data.get('research_interests')
            # if research_interests:
            #     # Assuming 'research_interests' is a comma-separated list of interests
            #     research_interests_list = research_interests.split(',')  # Split if input is comma-separated
            #     for interest in research_interests_list:
            #         # If the interest doesn't exist, create it
            #         interest_obj, created = ResearchInterest.objects.get_or_create(name=interest.strip())
            #         user_profile.research_interests.add(interest_obj)

            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'app/register.html', {'form': form})

@login_required
def landing_page(request):
    # return HttpResponse("<h1> Find hot papers in your area </h1>")
    return render(request, "index.html")

def preferences_page(request):
    reading_times = [15, 30, 45, 60, 75, 90, 105, 120]
    context = {'reading_times': reading_times}
    return render(request, "preferences.html", context)

def submit_preferences(request):
    if request.method == "POST":
        reading_time = request.POST.get('reading_time')
        difficulty_level = request.POST.get('difficulty_level')
        paper_recency = request.POST.get('paper_recency')
        research_interest = request.POST.get('research_interest')

        context = {
            'reading_time': reading_time,
            'difficulty_level': difficulty_level,
            'paper_recency': paper_recency,
            'research_interest': research_interest,
        }

        # return HttpResponse(f"Preferences Submitted: {reading_time}, {difficulty_level}, {paper_recency}, {research_interest}")
        return render(request, "summary.html", context)
    return redirect('landing_page')

def start_swiping(request):
    # Capture the preferences and save them to the database
    reading_time = request.POST.get('reading_time')
    difficulty_level = request.POST.get('difficulty_level')
    paper_recency = request.POST.get('paper_recency')
    research_interest_name = request.POST.get('research_interest')

    research_interest, created = ResearchInterest.objects.get_or_create(name=research_interest_name)

    user, created = User.objects.get_or_create(username="Guest")

    user_preference = UserPreference.objects.create(
        user=user,
        reading_time=reading_time,
        difficulty_level=difficulty_level,
        paper_recency=paper_recency,
        research_interest=research_interest
    )

    # Redirect to start swiping
    return redirect('swipe_papers') 

def swipe_papers(request):
    return render(request, "swipe_papers.html")


def paper_swipe_view(request):
    return render(request, 'paper_swipe.html')

def get_next_paper(request):
    # Get a random paper
    papers = list(Paper.objects.all())
    print(papers)
    if papers:
        paper = random.choice(papers)

        return JsonResponse({
            'title': paper.title,
            'content': paper.abstract
        })
    else:
        return JsonResponse({'message': 'No more papers available'}, status=404)

@require_POST
def rate_paper(request):
    paper_id = request.POST.get('paper_id')
    rating = request.POST.get('rating')
    
    if not paper_id or not rating:
        return JsonResponse({'status': 'error', 'message': 'Missing paper_id or rating'}, status=400)
    
    try:
        paper = Paper.objects.get(id=paper_id)
    except Paper.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Paper not found'}, status=404)
    
    # For now, just print the rating instead of saving it
    print(f"Paper {paper_id} rated as {rating}")
    
    return JsonResponse({'status': 'success'})

