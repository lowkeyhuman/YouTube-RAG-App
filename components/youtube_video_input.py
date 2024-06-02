import time
import streamlit as st
from services.youtube.youtube_service import get_video_details_from_url, get_video_id_from_url, get_youtube_transcript_from_youtube_video_id
from services.vector_database.vector_database_service import ingest_video_transcript

def youtube_video_input():
  with st.form('video_id_form'):
    col1, col2 = st.columns([4.8, 1])

    with col1:
      instruction = 'YouTube Video URL:'
      video_url = st.text_input(
        instruction,
        placeholder=instruction,
        label_visibility='collapsed'
      )

    with col2:
      video_url_button = st.form_submit_button('Ingest Video')

    if (video_url_button and video_url != ''):
      progress_bar = st.progress(0, text=f'getting video id from url: {video_url}')
      try:
        video_id = get_video_id_from_url(video_url)
      except:
        progress_bar.progress(2, text=f'❌ Failed to get video id from video url: {video_url}')
        return
      
      try:
        progress_bar.progress(5, text=f'fetching video detail from video url: {video_url}')
        video_details = get_video_details_from_url(video_url)
      except:
        progress_bar.progress(7, text=f'❌ Failed to video details from video url: {video_url}')
        return

      try:
        progress_bar.progress(10, text=f'fetching transcript from video id: {video_id}')
        transcript = get_youtube_transcript_from_youtube_video_id(video_id)
      except:
        progress_bar.progress(12, text=f'❌ Failed to fetch English transcript for video id: {video_id}')
        return

      progress_bar.progress(20, text=f'Ingesting transcript into vector database for video: {video_details.title}')
      try:
        ingest_video_transcript(transcript, video_id, video_details)
      except:
        progress_bar.progress(22, text=f'❌ Failed to ingest transcript into vector database for video: {video_details.title}')
        return

      progress_bar.progress(100, text=f'✅ Transcript ingestion completed for video: {video_details.title}')
      time.sleep(0.5)
      progress_bar.empty()