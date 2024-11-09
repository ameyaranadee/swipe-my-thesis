from django.contrib import admin
from .models import ResearchTopic, Author, User, Paper, Course

@admin.register(ResearchTopic)
class ResearchTopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'major')
    search_fields = ('name', 'university', 'major')
    filter_horizontal = ('papers_liked', 'courses')

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'research_topic', 'reading_time', 'difficulty_level', 'paper_recency')
    list_filter = ('research_topic', 'difficulty_level', 'paper_recency')
    search_fields = ('name', 'url')
    filter_horizontal = ('authors',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name')  # Display name and description in the list view
    search_fields = ('course_code', 'name')