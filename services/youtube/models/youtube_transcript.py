class YouTubeTranscriptLine:
  def __init__(self, text: str, start: float) -> None:
    self.text = text
    self.start = start

  def __repr__(self) -> str:
    return f"{{'text': {repr(self.text)}, 'start': {self.start}}}"