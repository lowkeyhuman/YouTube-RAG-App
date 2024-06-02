import math
from qdrant_client.models import QueryResponse

def sources_html(relevant_queryResponses: list[QueryResponse]) -> str:
  response = '\n\n\n ------------- \n\n\n #### Sources: \n\n'

  for queryResponse in relevant_queryResponses:
    video_title = queryResponse.metadata['source_video_title']
    start = math.floor(queryResponse.metadata['source_start'])
    url = f"https://youtu.be/{queryResponse.metadata['source_video_id']}?t={start}"

    response += f'1. ... {queryResponse.document} ... '
    response += f'\n\n\t**YouTube Video Title:** {video_title}'
    response += f'\n\n\t**YouTube Video URL:** {url}\n\n'

  return response