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


# @admin.register(ResearchTopic)
# class ResearchTopicAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name', )
#     search_fields = ('name', )

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'university', 'major')
#     search_fields = ('name', 'university', 'major')
#     filter_horizontal = ('papers_liked', 'courses')

# @admin.register(Paper)
# class PaperAdmin(admin.ModelAdmin):
#     list_display = ('name', 'url', 'research_topic', 'reading_time', 'difficulty_level', 'paper_recency')
#     list_filter = ('research_topic', 'difficulty_level', 'paper_recency')
#     search_fields = ('name', 'url')
#     filter_horizontal = ('authors',)

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('course_code', 'name')  # Display name and description in the list view
#     search_fields = ('course_code', 'name')