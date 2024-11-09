from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserPreference, ResearchInterest
from django.contrib.auth.models import User

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
