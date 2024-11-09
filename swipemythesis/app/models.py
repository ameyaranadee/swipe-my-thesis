from django.db import models

class ResearchTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Paper(models.Model):
    READING_TIME_CHOICES = [(i, f"{i} minutes") for i in range(15, 120, 15)]
    DIFFICULTY_LEVEL_CHOICES = [
        ('undergrad', 'Undergraduate'),
        ('grad', 'Graduate')
    ]
    PAPER_RECENCY_CHOICES = [
        ('6m', '6 months'),
        ('1yr', '1 year'),
        ('3yr', '3 years'),
        ('any', 'Anytime'),
    ]
    name = models.CharField(max_length=30)
    url = models.URLField()
    authors = models.ManyToManyField(Author)
    research_topic = models.ForeignKey(ResearchTopic, on_delete=models.CASCADE)
    reading_time = models.IntegerField(choices=READING_TIME_CHOICES)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL_CHOICES)
    paper_recency = models.CharField(max_length=3, choices=PAPER_RECENCY_CHOICES)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    course_code = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_code} - {self.name}"
    
class User(models.Model):
    name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='users')
    papers_liked = models.ManyToManyField(Paper, related_name='liked_by', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.name