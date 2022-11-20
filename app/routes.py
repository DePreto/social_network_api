import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.depends import get_crt_user, get_session, get_crt_tweet, get_crt_favorite
from app.utils import get_rnd_file_name_by_content_type
from app import schemas
from app import models


router = APIRouter()
out_file_path = os.environ.get("OUT_FILE_PATH")


@router.get("/")
def first_root():
    pass


@router.post("/api/tweets")
def post_tweet(
        data: schemas.TweetSchema,
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    tweet = models.Tweet(user_id=user.id, post=data.tweet_data)
    session.add(tweet)
    session.flush()

    for media_id in data.tweet_media_ids:
        media = session.query(models.Media).filter_by(id=media_id).one_or_none()
        if not media:
            raise HTTPException(status_code=404, detail=f"media {media_id} not found")

        post_media = models.tweet_media.insert().values({"tweet_id": tweet.id, "media_id": media_id})
        session.execute(post_media)

    session.commit()

    return {
        "result": True,
        "tweet_id": tweet.id
    }


@router.post("/api/medias")
def post_medias(
        file: UploadFile,
        session: Session = Depends(get_session)
):
    file_name = get_rnd_file_name_by_content_type(file.content_type)
    file_path = os.path.join(out_file_path, file_name)
    try:
        with open(file_path, 'wb') as out_file:
            content = file.file.read()
            out_file.write(content)
    except IOError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    else:
        media = models.Media(path=file_path)
        session.add(media)

    session.commit()

    return {
        "result": True,
        "media_id": media.id,
    }


@router.delete("/api/tweets/{id}")
def delete_tweet(
        user: models.User = Depends(get_crt_user),
        tweet: models.Tweet = Depends(get_crt_tweet),
        session: Session = Depends(get_session)
):
    if user.id == tweet.user_id:
        session.delete(tweet)
        session.commit()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/api/tweets/{id}/likes")
def post_like(
        tweet: models.Tweet = Depends(get_crt_tweet),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    favourite_exist = session.query(models.Favorite).filter_by(user_id=user.id, tweet_id=tweet.id).one_or_none()
    if not favourite_exist:
        favourite = models.Favorite(user_id=user.id, tweet_id=tweet.id)
        session.add(favourite)
        session.commit()


@router.delete("/api/tweets/{id}/likes")
def delete_like(
        favourite: models.Favorite = Depends(get_crt_favorite),
        session: Session = Depends(get_session)
):
    session.delete(favourite)
    session.commit()


@router.post("/api/users/{id}/follow")
def post_follow(
        following_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):

    following_user = session.query(models.User).filter_by(id=following_id).one_or_none()
    following = session.query(models.user_following).filter_by(user_id=user.id, following_id=following_id).one_or_none()

    if not following_user:
        raise HTTPException(status_code=404, detail="Following user not found")
    elif following_id == user.id:
        pass
    elif not following:
        user_following = models.user_following.insert().values({"user_id": user.id, "following_id": following_id})
        session.execute(user_following)
        session.commit()


@router.delete("/api/users/{id}/follow")
def delete_follow(
        following_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    following = session.query(models.user_following).filter_by(user_id=user.id, following_id=following_id).one_or_none()

    if following:
        delete_stmt = delete(models.user_following).where(
            models.user_following.c.user_id == user.id,
            models.user_following.c.following_id == following_id
        )

        session.execute(delete_stmt)
        session.commit()

    else:
        raise HTTPException(status_code=404, detail="Following not found")


@router.get("/api/tweets")
def get_tweets():
    pass


@router.get("/api/users/me")
def get_me():
    pass


@router.get("/api/users/{id}")
def get_user(user_id: int = Path(alias="id")):
    pass
