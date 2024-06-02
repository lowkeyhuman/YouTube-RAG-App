import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from services.youtube.models.youtube_transcript import YouTubeTranscriptLine
from services.youtube.models.youtube_video_details import YouTubeVideoDetails

def get_video_id_from_url(url: str) -> str:
  regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
  match = re.search(regex, url)
  if match:
      return match.group(1)
  raise Exception('Failed to get video id')

def get_video_details_from_url(url: str) -> YouTubeVideoDetails:
  api_url = f'https://noembed.com/embed?url={url}'
  response = requests.get(api_url)
  response.raise_for_status()
  data = response.json()

  title = data.get('title', None)
  author = data.get('author_name', None)

  return YouTubeVideoDetails(title, author) 

def get_youtube_transcript_from_youtube_video_id(video_id: str) -> list[YouTubeTranscriptLine]:
  transcript = YouTubeTranscriptApi.get_transcript(
    video_id=video_id,
    languages=['en', 'en-US']
  )

  transcript = [YouTubeTranscriptLine(line['text'], line['start']) for line in transcript]
  transcript = remove_music(transcript)
  transcript = join_youtube_transcripts(transcript)

  return transcript

def remove_music(transcript: list[YouTubeTranscriptLine]) -> list[YouTubeTranscriptLine]:
  updated_transcript = [line for line in transcript if 
                        (
                          not (line.text.startswith('[')) and 
                          not (line.text.endswith(']')) 
                        ) or (' ' in line.text)]
  
  return updated_transcript

def join_youtube_transcripts(transcript: list[YouTubeTranscriptLine], min_words_per_line: int = 50) -> list[YouTubeTranscriptLine]:
  updated_transcript = []

  current_line_text = ''
  current_line_start = 0
  for i in range(len(transcript)):
    if (current_line_text == ''):
      current_line_text = transcript[i].text
      current_line_start = transcript[i].start
    elif (get_word_count(current_line_text) < min_words_per_line):
      current_line_text = current_line_text + ' ' + transcript[i].text

    if (get_word_count(current_line_text) >= min_words_per_line):
      new_line = YouTubeTranscriptLine(
        text=current_line_text, 
        start=current_line_start)
      
      updated_transcript.append(new_line)
      current_line_text = ''

  if (current_line_text != ''):
    new_line = YouTubeTranscriptLine(
      text=current_line_text, 
      start=current_line_start)
    
    updated_transcript.append(new_line)
    current_line_text = ''
  
  return updated_transcript

def get_word_count(text: str) -> int:
  return len(text.split(' '))