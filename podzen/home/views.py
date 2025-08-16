import re
import requests
import os
import json
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from urllib.parse import quote, unquote
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

load_dotenv()

def home_view(request):
    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        if youtube_link:
            return get_video_link(request, link=youtube_link)
    return render(request, 'home/home.html')

def get_ai_answer(transcript):
    API_KEY = os.environ.get('API_KEY')
    url = "https://api.perplexity.ai/chat/completions"  # Confirm from docs

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "user",
                "content": f"Read the following text carefully and extract at  10 of the most important questions and their concise answers. Structure the output in a python list format where each entry has a question and next its answer [question1,answer1,qyuestion2,answer2]. Keep the answers short, clear, and to the point. give list directly no extra things in data :\n\n{transcript}"
            }
        ],
        "max_tokens": 5000
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error:{response} {response.status_code} {response.text}"


def get_transcript_from_url(youtube_url="https://www.youtube.com/watch?v=ugqVaSOfR5g", language_code='en'):
    """
    Retrieves the transcript for a given YouTube URL.

    Args:
        youtube_url (str): The full URL of the YouTube video.
        language_code (str): The language code for the desired transcript (e.g., 'en', 'es', 'fr').

    Returns:
        str: The full transcript text, or an error message.
    """
    try:
        # Extract video ID from URL
        parsed_url = urlparse(youtube_url)
        if 'youtube.com' in parsed_url.netloc:
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        elif 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path[1:]
        else:
            return "Error: Invalid YouTube URL."

        if not video_id:
            return "Error: Could not extract video ID from URL."

        ytt_api = YouTubeTranscriptApi()       
        
        # Fetch the actual transcript data
        fetched_transcript = ytt_api.fetch(video_id)
        script=[]
        for snippet in fetched_transcript:
            script.append(snippet.text)
        # Combine the text parts into a single string
        full_transcript = " ".join(script)

        return full_transcript

    
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_video_link(request, link):
    
    try:
        transcipt = get_transcript_from_url(link)
        print("got transcript",len(transcipt))
        ai_answer =   get_ai_answer(transcipt)
        print("got ai answer",len(ai_answer),ai_answer)
        # Example JSON string
        json_string = ai_answer   

        # Convert JSON string → Python object (list of dicts)
        data = json.loads(json_string)
        data = [{'question':data[i],'answer':data[i+1]} for i in range(0,len(data)-1,2)]
        print("clean answer",len(data),data)
        
        return render(request, 'home/show_answer.html', {"data":data})
    except Exception as e:
        return render(request, 'home/show_answer.html', {"data":f"ERROR: {e}"})



