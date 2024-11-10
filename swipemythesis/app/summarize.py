import re
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration
from celery import shared_task
from .models import Paper, ResearchInterest


@shared_task
def call_summarize_main_function(paper_title, url):
    print('Letssss goooooooooooo')
    model, tokenizer, device=load_model()
    final(model, tokenizer, device, url, paper_title)

def load_model():
# Load the tokenizer and model
    model_name = "allenai/led-base-16384"  # Use a smaller model if necessary for speed

    # Initialize tokenizer and model
    tokenizer = LEDTokenizer.from_pretrained(model_name)
    model = LEDForConditionalGeneration.from_pretrained(model_name).half()  # Enable FP16 for faster inference

    # Move model to GPU if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    return model, tokenizer, device

def return_text(url):
    url = url.replace("abs", "pdf")
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.headers['Content-Type'] == 'application/pdf':
        try:
            pdf = PdfReader(BytesIO(response.content))
            text = ''
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading the PDF: {e}")
            return None
    else:
        print("The URL did not return a PDF file.")
        return None

def postprocess_text(text):
    # General clean-up using regular expressions
    text = re.sub(r'[�𒏻]', '', text)  # Remove unwanted characters
    text = re.sub(r'[@#$%&*]{3,}', '', text)  # Remove long sequences of special characters
    text = re.sub(r'(\s{2,})', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\n{2,}', '\n', text)  # Replace multiple newlines with a single newline

    # Remove lines with underscores and citation markers
    text = re.sub(r'_{5,}', '', text)  # Remove long sequences of underscores
    text = re.sub(r'\[\d+\]', '', text)  # Remove citation markers like [41]

    # Remove headers/footers and repeated sections
    text = re.sub(r'(Corresponding author:.*?Creative Commons Attribution Liscense 4.0\.)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(Received on .*? accepted on .*?)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(World Journal of Advanced Research and Reviews,.*?[-–]\d+\n?)', '', text, flags=re.IGNORECASE)

    # Detect and fix broken words at line breaks
    text = re.sub(r'-\s*\n', '', text)  # Join words split by hyphen and newline
    text = re.sub(r'\n([a-z])', r' \1', text)  # Fix lowercase letters starting new lines incorrectly

    # Format bullet points and sections
    text = re.sub(r'▬', '\n- ', text)  # Standardize section markers
    text = re.sub(r'(\n\s*-\s*)+', '\n- ', text)  # Remove excessive dashes or markers

    # Ensure clean spacing around punctuation and sentence capitalization
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'([.,;:!?])(?=[A-Za-z])', r'\1 ', text)  # Add space after punctuation if needed
    text = '. '.join([sentence.strip().capitalize() for sentence in text.split('. ')])  # Capitalize sentences

    return text.strip()


def summarize_text(text, model, tokenizer, device):
    # Split text into manageable chunks
    chunk_size = 5000  # Adjust for preference
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []
    with torch.no_grad():  # Disable gradient calculations for inference
        for chunk in chunks:
            inputs = tokenizer(
                chunk,
                return_tensors="pt",
                max_length=16384,
                truncation=True
            ).to(device)  # Move tensors to GPU if available

            # Generate summary
            summary_ids = model.generate(
                inputs.input_ids,
                max_length=256,  # Shorter length for faster processing
                min_length=50,
                length_penalty=2.0,
                num_beams=2,  # Reduced beams for speed
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            
            # Decode the summary
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

    # Combine summaries from all chunks
    return postprocess_text(" ".join(summaries))

def final(model, tokenizer, device, url, paper_title):
    # url = "http://arxiv.org/abs/2410.20281v1"  # Example URL
    text = return_text(url)

    if text:
        summary = summarize_text(text, model, tokenizer, device)
        paper = Paper.objects.get(title = paper_title)
        paper.paper_summary=summary
        paper.save()
        print("Summary:\n")
        print(summary)
    else:
        print("Failed to extract text from the PDF.")