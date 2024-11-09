import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from transformers import pipeline

def load_model():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return classifier

def difficulty_level(classifier, text):
    labels = ["basic research paper", "advanced research paper"]
    result = classifier(text, labels)

    classification = result['labels'][0]
    score = result['scores'][0]

    return classification, score

def approximate_reading_time(paper_text, difficulty):
    word_count = len(paper_text.split())
    
    if difficulty == "basic research paper":
        reading_speed = 200 
    else:
        reading_speed = 150

    reading_time = word_count / reading_speed

    return reading_time

def return_text(url):
    url = url.replace("abs", "pdf")

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    if response.headers['Content-Type'] == 'application/pdf':
        try:
            # Read and parse the PDF
            pdf = PdfReader(BytesIO(response.content))
            text = ''
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

            return text
        except Exception as e:
            print(f"Error reading the PDF: {e}")
    else:
        print("The URL did not return a PDF file.")
      
def find_sorted_closest_indexes(target, numbers):
    differences = [(i, abs(num - target)) for i, num in enumerate(numbers)]
    sorted_differences = sorted(differences, key=lambda x: x[1])
    sorted_indexes = [index for index, _ in sorted_differences]
    
    return sorted_indexes   
    
def search_arxiv_and_parse(classifier, query, max_results=5, timespan=1000000, target_reading=120, diff_lv='Basic'):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

    root = ET.fromstring(response.text)
    ns = {'ns': 'http://www.w3.org/2005/Atom'}
    
    data = []
    count = 0
    reading_times = []
    for entry in root.findall('ns:entry', ns):
        title = entry.find('ns:title', ns).text.strip()
        summary = entry.find('ns:summary', ns).text.strip()
        published = entry.find('ns:published', ns).text.strip()
        published = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
        link = entry.find('ns:id', ns).text.strip()
        data.append({
            'Title': title,
            'Summary': summary,
            'Published Date': published,
            'Link': link
        })
    
    data = sorted(data, key=lambda x: x['Published Date'], reverse = True)
    
    for title, summary, published, link in zip([item['Title'] for item in data],
                                [item['Summary'] for item in data],
                                [item['Published Date'] for item in data],
                                [item['Link'] for item in data]):
            
        today = datetime.today()
        difference = (today - published).days
        if difference < timespan:
            print(difference)
            text = return_text(link)
            difficulty = difficulty_level(classifier, text)
            print(difficulty)
            if diff_lv.lower() in difficulty[0]:
                read_time = approximate_reading_time(text, difficulty)
                reading_times.append(read_time)
                data.append({
                    'Title': title,
                    'Summary': summary,
                    'Published Date': published,
                    'Link': link
                })
                count += 1
                if count >= 5:
                    sorted_indexes = find_sorted_closest_indexes(target_reading, reading_times)
                    count = 0
                    reading_times=[]
                    sorted_data = [data[i] for i in sorted_indexes]
                    print(sorted_data)
        else:
            break

classifier = load_model()
search_arxiv_and_parse(classifier, query="machine learning", max_results=500, timespan=180, target_reading=120, diff_lv='Advanced')