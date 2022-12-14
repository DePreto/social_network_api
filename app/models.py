from typing import List

from sqlalchemy import Column, DateTime, Text, Integer, ForeignKey, Table, PrimaryKeyConstraint, CheckConstraint
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
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    favorites = relationship("Favorite", backref="tweet", cascade="all, delete", uselist=True, lazy="selectin")
    media = relationship("Media", secondary=tweet_media, uselist=True, lazy="selectin")

    __mapper_args__ = {"eager_defaults": True}


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


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    key = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    following: List = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        uselist=True,
        lazy="selectin"
    )

    followers: List = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.following_id,
        secondaryjoin=lambda: User.id == user_following.c.user_id,
        uselist=True,
        lazy="selectin"
    )

    tweets: List[Tweet] = relationship("Tweet", backref="user", uselist=True, lazy="selectin")
    favorites: List[Favorite] = relationship("Favorite", backref="user", uselist=True)

    __mapper_args__ = {"eager_defaults": True}


user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id), primary_key=True),
    CheckConstraint('user_id <> following_id'),
    PrimaryKeyConstraint('user_id', 'following_id')
)
