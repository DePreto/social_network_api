from sqlalchemy import ARRAY, Column, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db.base import Base


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post = Column(Text)
    favorites_count = Column(Integer, nullable=False, server_default="0")
    replies_count = Column(Integer, nullable=False, server_default="0")
    retweets_count = Column(Integer, nullable=False, server_default="0")
    tags = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    favorites = relationship("Favorite", backref="tweet")
    retweets = relationship("Retweet", backref="tweet")
    replies = relationship("Reply", backref="tweet")
    taggings = relationship("Tagging", backref="tweet")


class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))


class Retweet(Base):
    __tablename__ = "retweet"

    retweet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))


class Reply(Base):
    __tablename__ = "reply"

    reply_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))
    post = Column(Text)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    key = Column(Text, nullable=False)
    favorites_count = Column(Integer, nullable=False, server_default="0")
    followers_count = Column(Integer, nullable=False, server_default="0")
    following_count = Column(Integer, nullable=False, server_default="0")
    tweets_count = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    tweets = relationship("Tweet", backref="user")
    favorites = relationship("Favorite", backref="user")
    # followers = relationship("Follower.user_id", backref="user")  # TODO
    # following = relationship("Follower.follower_id", backref="follower")  # TODO


class Follower(Base):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    follower_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Tagging(Base):
    __tablename__ = 'tagging'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(Integer, ForeignKey("tweet.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    tweets = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    taggings = relationship("Tagging", backref="tag")
