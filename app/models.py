from typing import List

from sqlalchemy import ARRAY, Column, DateTime, Text, Integer, ForeignKey, Table, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db.base import Base


tweet_media = Table(
    "tweet_media",
    Base.metadata,
    Column("tweet_id", ForeignKey("tweet.id")),
    Column("media_id", ForeignKey("media.id")),
    PrimaryKeyConstraint("tweet_id", "media_id")
)


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

    favorites = relationship("Favorite", backref="tweet", cascade="all, delete", uselist=True)
    retweets = relationship("Retweet", backref="tweet", cascade="all, delete", uselist=True)  # TODO rm
    replies = relationship("Reply", backref="tweet", cascade="all, delete", uselist=True)  # TODO rm
    taggings = relationship("Tagging", backref="tweet", cascade="all, delete", uselist=True)  # TODO rm
    media = relationship("Media", secondary=tweet_media, uselist=True)


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Text)


class Favorite(Base):
    __tablename__ = "favorite"

    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))

    __table_args__ = (
        PrimaryKeyConstraint(user_id, tweet_id),
    )


class Retweet(Base):  # TODO rm
    __tablename__ = "retweet"

    retweet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))


class Reply(Base):  # TODO rm
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

    following: List = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers',
        uselist=True,
    )

    tweets: List[Tweet] = relationship("Tweet", backref="user", uselist=True)
    favorites: List[Favorite] = relationship("Favorite", backref="user", uselist=True)


user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id), primary_key=True),
    CheckConstraint('user_id <> following_id'),
    PrimaryKeyConstraint('user_id', 'following_id')
)


class Tagging(Base):  # TODO rm
    __tablename__ = 'tagging'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(Integer, ForeignKey("tweet.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Tag(Base):  # TODO rm
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    tweets = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    taggings = relationship("Tagging", backref="tag", uselist=True)
