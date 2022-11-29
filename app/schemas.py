from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List


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


class UserSchema(AuthorSchema):
    followers: List[AuthorSchema]
    following: List[AuthorSchema]


class FavoriteSchemaIn(BaseModel):
    user: AuthorSchema

    class Config:
        orm_mode = True


class FavoriteSchemaOut(AuthorSchema):
    id: int = Field(alias="user_id")


class TweetSchema(BaseModel):
    id: int


class TweetSchemaIn(TweetSchema):
    content: str = Field(alias="post")
    attachments: List[MediaSchema] = Field(alias="media")
    author: AuthorSchema = Field(alias="user")
    likes: List[FavoriteSchemaIn] = Field(alias="favorites")

    class Config:
        orm_mode = True
        json_encoders = {
            MediaSchema: lambda m: m.path,
            FavoriteSchemaIn: lambda f: f.user.dict()
        }


class TweetSchemaOut(TweetSchema):
    content: str
    attachments: List[str]
    author: AuthorSchema
    likes: List[FavoriteSchemaOut]


class FeedSchemaOut(BaseModel):
    result: bool
    tweets: List[TweetSchemaOut]


class DefaultSchema(BaseModel):
    result: bool = True


class PageSchema(BaseModel):
    result: bool
    user: UserSchema
