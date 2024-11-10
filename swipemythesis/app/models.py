from django.db import models
from django.contrib.auth.models import User

class ResearchInterest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # password= models
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    university = models.CharField(max_length=255)
    major = models.CharField(max_length=100)
    courses = models.TextField(help_text="Comma-separated list of courses")
    research_interests = models.ManyToManyField(ResearchInterest, related_name="users")

    def __str__(self):
        return self.user.username

class Paper(models.Model):
    title = models.CharField(max_length=255, null=True)
    abstract = models.TextField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    authors = models.CharField(max_length=255, null=True)
    url = models.URLField()
    research_interest = models.ForeignKey(ResearchInterest, on_delete=models.CASCADE, related_name="papers",null=True, blank=True)
    paper_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_time = models.IntegerField(choices=[(i, f"{i} minutes") for i in range(15, 121, 15)])
    difficulty_level = models.CharField(max_length=20)
    paper_recency = models.IntegerField()
    research_interest = models.ForeignKey(ResearchInterest, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return f"Preferences of {self.user.username}"

class UserLikedPapers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_papers")
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="liked_by_users")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'paper')  # Ensure each paper can be liked only once per user

    def __str__(self):
        return f"{self.user.username} liked {self.paper.title}"
