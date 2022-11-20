from pydantic import BaseModel
from typing import List


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] = []
