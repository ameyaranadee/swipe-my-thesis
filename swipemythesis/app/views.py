from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserPreference, ResearchInterest
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Paper
from django.views.decorators.http import require_POST
import random

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

