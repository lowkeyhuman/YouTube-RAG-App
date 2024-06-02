from services.youtube.models.youtube_transcript import YouTubeTranscriptLine
from services.youtube.models.youtube_video_details import YouTubeVideoDetails
from qdrant_client import QdrantClient
from qdrant_client.models import QueryResponse

QDRANT_COLLECTION_NAME = 'YouTube_RAG_App'

client = QdrantClient(":memory:")

def ingest_video_transcript(transcript: list[YouTubeTranscriptLine], video_id: str, video_details: YouTubeVideoDetails) -> None:
  documents = [line.text for line in transcript]
  metadata = [
    {
      'source_video_id': video_id,
      'source_video_title': video_details.title,
      'source_start': line.start
    }
    for line in transcript
  ]

  client.add(
      collection_name=QDRANT_COLLECTION_NAME,
      documents=documents,
      metadata=metadata,
  )

def similarity_search(query: str, limit:int=10) -> list[QueryResponse]:
  response = client.query(
    collection_name=QDRANT_COLLECTION_NAME,
    query_text=query,
    limit=limit
  )
  return response