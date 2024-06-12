from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os
from dotenv import load_dotenv 
import openai as ai
import yt_dlp
import assemblyai as aai


load_dotenv()

def yt_title(link):
    video_id = link.split('=')[-1]
    title_complete = extract_youtube_title(video_id)
    return title_complete

def extract_youtube_title(video_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={os.getenv('youtube_api_key')}"
        response = requests.get(url)
        data = response.json()
        title = data['items'][0]['snippet']['title']
        return title
    except Exception as e:
        return None
    

def yt_subtitle(link):
    video_id = link.split('=')[-1]
    if (video := extract_youtube_subtitle(video_id)) != None:
        return video
    else:
        return get_transcript(video_id)

def extract_youtube_subtitle(video_id) -> str:
    try:
        li = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        if (len(li)) == 0:
            raise Exception('No transcript found')
    except Exception as e:
        return None

    return (' '.join([i['text'] for i in li]))


def generateContent(transcript):
    ai.api_key = os.getenv('openai_api_key')
    response = ai.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        max_tokens = 1000,
        messages = [
            {'role': 'assistant', 'content': transcript},
            {'role': 'user', 'content': 'write a comprehensive blog article, without the title, it should be just long paragraph without introduction point thing'}
        ]
    )
    return response.choices[0].message.content


def audio_link(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'media/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        audio_file = f'media/{info["title"]}.mp3'
    return audio_file


def get_transcript(link):
    audio_file = audio_link(link)
    aai.settings.api_key = os.getenv('assembly_ai_api_key')

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text


def chat_response(message, data):
    ai.api_key = os.getenv('openai_api_key')
    response =  response = ai.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        max_tokens = 1000,
        messages = [
            {'role': 'assistant', 'content': data},
            {'role': 'user', 'content': message}
        ]
    )
    return response.choices[0].message.content