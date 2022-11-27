from pydantic import BaseModel, Field
from typing import List, Optional, Union


class PostTweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] = []


class MediaSchema(BaseModel):
    path: str

    class Config:
        orm_mode = True

    def dict(
        self, *args, **kwargs
    ) -> str:
        return self.path


class AuthorSchema(BaseModel):
    id: int
    username: str = Field(alias="name")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FavoriteSchema(BaseModel):
    user: AuthorSchema

    class Config:
        orm_mode = True

    def dict(self, *args, **kwargs) -> dict:
        return {
            "user_id": self.user.id,
            "name": self.user.username,
        }


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


class DefaultSchema(BaseModel):
    result: bool = True
