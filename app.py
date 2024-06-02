import streamlit as st
from components.assistant_response import generate_response
from components.youtube_video_input import youtube_video_input

# sidebar
with st.sidebar:
  response_source_count = st.number_input(
    label='Response Source Count', 
    min_value = 1, 
    max_value = 30, 
    value=5
  )

  show_sources = st.toggle('Show Sources', value=True)

# populate session state
if 'messages' not in st.session_state:
  st.session_state['messages'] = [
    {'role': 'assistant', 'content': "Hi, I'm a chatbot who can answer questions about a particular YouTube video. \n \n How can I help you?"}
  ]

# title
st.title('YouTube RAG App')

# youtube video ingest section
youtube_video_input()

# write chat history
for msg in st.session_state.messages:
  st.chat_message(msg['role']).markdown(msg['content'])

query = st.chat_input(
  placeholder='Ask a question about the ingested video'
)

if query:
  st.session_state.messages.append({'role': 'user', 'content': query})
  st.chat_message('user').markdown(query)

  with st.spinner('thinking...'):
    response = generate_response(query, response_source_count, show_sources)

  st.session_state.messages.append({'role': 'assistant', 'content': response})
  st.chat_message('assistant').markdown(response, unsafe_allow_html=True)