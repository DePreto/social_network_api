from db.session import Session
from fastapi import Path, Header, Depends, HTTPException

from app import models


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_crt_user(
        api_key: str = Header(default=None, alias="api-key"),
        session: Session = Depends(get_session)
):
    user = session.query(models.User).filter_by(key=api_key).one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


def get_crt_tweet(
    tweet_id: int = Path(alias="id"),
    session: Session = Depends(get_session),
):
    tweet = session.query(models.Tweet).filter_by(id=tweet_id).one_or_none()
    if tweet:
        return tweet
    else:
        raise HTTPException(status_code=404, detail="Tweet not found")


def get_crt_favorite(
        tweet_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    favorite = session.query(models.Favorite).filter_by(user_id=user.id, tweet_id=tweet_id).one_or_none()
    if favorite:
        return favorite
    else:
        raise HTTPException(status_code=404, detail="Like not found")


def get_user_by_id(
        user_id: int = Path(alias="id"),
        session: Session = Depends(get_session)
):
    user = session.query(models.User).filter_by(id=user_id).one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='User not found')

