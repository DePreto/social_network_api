from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError, validator
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


class DefaultSuccessSchema(BaseModel):
    result: bool = True

    @validator("result")
    def result_is_true(cls, value):
        if value is not True:
            raise ValidationError("success result should be True")
        return value


class FeedSchemaOut(DefaultSuccessSchema):
    tweets: List[TweetSchemaOut]


class PageSchema(DefaultSuccessSchema):
    user: UserSchema


class PostTweetResponseSchema(DefaultSuccessSchema):
    tweet_id: int


class PostMediaResponseSchema(DefaultSuccessSchema):
    media_id: int


class DefaultExceptionContentSchema(BaseModel):
    result: bool
    error_type: str
    error_message: str

    @validator("result")
    def result_is_true(cls, value):
        if value is not False:
            raise ValidationError("success result should be False")
        return value


class DefaultExceptionSchema(BaseModel):
    status_code: int
    content: DefaultExceptionContentSchema
