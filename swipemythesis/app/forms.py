from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, ResearchInterest

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    university = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your university'}))
    profile_picture = forms.ImageField(required=True)
    major = forms.CharField(max_length=255, required=True)
    courses = forms.CharField(widget=forms.Textarea, required=True)
    research_interests = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and modify help text
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        
        # Simplify the password help text
        self.fields['password1'].help_text = 'Must be 8+ characters with numbers and letters'

        # Add placeholders for new fields
        self.fields['university'].widget.attrs['placeholder'] = 'University'
        self.fields['profile_picture'].widget.attrs['placeholder'] = 'Profile Picture'
        self.fields['major'].widget.attrs['placeholder'] = 'Your Major'
        self.fields['courses'].widget.attrs['placeholder'] = 'List of Courses'
        self.fields['research_interests'].widget.attrs['placeholder'] = 'Your Research Interests'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        # Create and save the UserProfile
        profile = UserProfile(
            user=user,
            profile_picture=self.cleaned_data['profile_picture'],
            university=self.cleaned_data['university'],
            major=self.cleaned_data['major'],
            courses=self.cleaned_data['courses']
        )
        profile.save()

        # Handle research interests (assuming comma-separated input)
        research_interests = self.cleaned_data['research_interests']
        if research_interests:
            research_interests_list = research_interests.split(',')
            for interest in research_interests_list:
                interest_obj, created = ResearchInterest.objects.get_or_create(name=interest.strip())
                profile.research_interests.add(interest_obj)

        return user

