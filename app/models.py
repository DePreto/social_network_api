from uuid import uuid4

from sqlalchemy import ARRAY, Column, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    post = Column(Text)
    favorites_count = Column(Integer, nullable=False, server_default="0")
    replies_count = Column(Integer, nullable=False, server_default="0")
    retweets_count = Column(Integer, nullable=False, server_default="0")
    tags = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    favorites = relationship("Favorites", backref="tweet")
    retweets = relationship("Retweets", backref="tweet")
    replies = relationship("Replies", backref="tweet")
    taggings = relationship("Taggings", backref="tweet")


class Favorites(Base):
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("tweets.id"))


class Retweets(Base):
    __tablename__ = "retweets"

    retweet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("tweets.id"))


class Replies(Base):
    __tablename__ = "replies"

    reply_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("tweets.id"))
    post = Column(Text)


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(Text, nullable=False)
    favorites_count = Column(Integer, nullable=False, server_default="0")
    followers_count = Column(Integer, nullable=False, server_default="0")
    following_count = Column(Integer, nullable=False, server_default="0")
    tweets_count = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    tweets = relationship("Tweets", backref="user")
    favorites = relationship("Favorites", backref="user")
    followers = relationship("Followers.user_id", backref="user")  # TODO
    following = relationship("Followers.follower_id", backref="follower")  # TODO


class Followers(Base):
    __tablename__ = "followers"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Taggings(Base):
    __tablename__ = 'taggings'

    id = Column(UUID(as_uuid=True), primary_key=True)
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("tweets.id"))
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"))


class Tags(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=False)
    tweets = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    taggings = relationship("Taggings", backref="tag")
