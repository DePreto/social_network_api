from pydantic import BaseModel, Field
from typing import List, Optional


class PostTweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] = []


class MediaSchema(BaseModel):
    path: str

    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    id: int
    username: str = Field(alias="name")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FavoriteSchema(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class TweetSchema(BaseModel):
    id: int
    post: str = Field(alias="content")
    media: List[MediaSchema] = Field(alias="attachments")
    user: AuthorSchema = Field(alias="author")
    favorites: List[FavoriteSchema] = Field(alias="likes")  # TODO name?

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FeedSchema(BaseModel):
    result: bool
    tweets: List[TweetSchema]
