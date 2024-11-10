from django.contrib import admin
# from .models import ResearchTopic, Author, User, Paper, Course
from django.contrib import admin
from .models import UserProfile, Paper, ResearchInterest, UserPreference, UserLikedPapers

# UserProfile admin to display profile details
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'major')
    search_fields = ('user__username', 'university', 'major')
    list_filter = ('research_interests',)

# Paper admin to manage research paper entries
@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'research_interest')
    search_fields = ('title', 'abstract', 'authors')
    list_filter = ('published_date', 'research_interest')
    ordering = ('-published_date',)

# ResearchInterest admin to manage available research areas
@admin.register(ResearchInterest)
class ResearchInterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# UserPreference admin to view user preferences
@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'reading_time', 'difficulty_level', 'paper_recency', 'research_interest')
    list_filter = ('difficulty_level', 'paper_recency', 'research_interest')
    search_fields = ('user__username',)

# UserLikedPapers admin to see all likes by users
@admin.register(UserLikedPapers)
class UserLikedPapersAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'timestamp')
    search_fields = ('user__username', 'paper__title')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)