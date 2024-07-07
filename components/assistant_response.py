from langchain_openai import ChatOpenAI
from components.sources_html import sources_html
from services.vector_database.vector_database_service import similarity_search
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = '''
Answer the question based only on the following context. 
The context is a list of transcript lines from one or more youtube videos.
The context: {context}

---
Answer the question based on the above context.
The question: {question}
'''

def generate_response(query: str, response_source_count: int, show_sources: bool, openai_api_key: str) -> str:
  try:
    relevant_queryResponses = similarity_search(query, response_source_count)
  except:
    return '⚠️ No video transcript found. Please ingest video (at the top)'

  context_text = '\n\n---\n\n'.join([queryResponse.document for queryResponse in relevant_queryResponses])
  prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = prompt_template.format(context=context_text, question=query)

  llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=openai_api_key)
  baseMessage = llm.invoke(prompt)
  response = baseMessage.content

  if show_sources:
    response += sources_html(relevant_queryResponses)
  
  return response