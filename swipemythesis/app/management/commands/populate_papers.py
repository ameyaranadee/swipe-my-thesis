from django.core.management.base import BaseCommand
from app.models import ResearchPaper

class Command(BaseCommand):
    help = 'Populates the database with sample research papers'

    def handle(self, *args, **kwargs):
        sample_papers = [
            {
                'title': 'The Effects of Climate Change on Biodiversity',
                'content': 'This paper explores the various ways in which global climate change impacts biodiversity across different ecosystems...'
            },
            {
                'title': 'Advancements in Quantum Computing',
                'content': 'Recent developments in quantum computing have opened up new possibilities for solving complex computational problems...'
            },
            {
                'title': 'The Role of Artificial Intelligence in Healthcare',
                'content': 'This study examines the current and potential future applications of AI in various aspects of healthcare, including diagnosis and treatment...'
            },
            {
                'title': 'Exploring Dark Matter in the Universe',
                'content': 'Dark matter remains one of the most enigmatic components of our universe. This paper reviews recent observations and theories...'
            },
            {
                'title': 'The Impact of Social Media on Mental Health',
                'content': 'This research investigates the relationship between social media usage and various aspects of mental health, including anxiety and depression...'
            },
        ]

        for paper in sample_papers:
            ResearchPaper.objects.create(title=paper['title'], content=paper['content'])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample papers'))