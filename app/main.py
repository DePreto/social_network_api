import os
import uuid

from fastapi import FastAPI, Path, Header, Depends, UploadFile, HTTPException
from app import models, schemas
from db.session import Session
from sqlalchemy import delete

import uvicorn

out_file_path = os.environ.get("OUT_FILE_PATH")


def get_rnd_file_name_by_content_type(content_type):
    return '.'.join([uuid.uuid4().hex, content_type.split("/")[-1]])


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
    user: models.User = Depends(get_crt_user)
):
    tweet = session.query(models.Tweet).filter_by(id=tweet_id, user_id=user.id).one_or_none()
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


app = FastAPI(dependencies=[Depends(get_crt_user)])


@app.get("/")
def first_root():
    return {"Hello": "1World"}


@app.post("/api/tweets")
def post_tweet(
        data: schemas.TweetSchema,
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    tweet = models.Tweet(user_id=user.id, post=data.tweet_data)
    session.add(tweet)
    session.flush()
    for media_id in data.tweet_media_ids:
        post_media = models.tweet_media.insert().values({"tweet_id": tweet.id, "media_id": media_id})
        session.execute(post_media)

    session.commit()

    return {
        "result": True,
        "tweet_id": tweet.id
    }


@app.post("/api/medias")
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


@app.delete("/api/tweets/{id}")
def delete_tweet(
        tweet: models.Tweet = Depends(get_crt_tweet),
        session: Session = Depends(get_session)
):
    session.delete(tweet)
    session.commit()

    return {
        "result": True
    }


@app.post("/api/tweets/{id}/likes")
def post_like(
        tweet_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    favourite = models.Favorite(user_id=user.id, tweet_id=tweet_id)
    session.add(favourite)
    session.commit()

    return {
        "result": True
    }


@app.delete("/api/tweets/{id}/likes")
def delete_like(
        favourite: models.Favorite = Depends(get_crt_favorite),
        session: Session = Depends(get_session)
):
    session.delete(favourite)
    session.commit()

    return {
        "result": True
    }


@app.post("/api/users/{id}/follow")
def post_follow(
        following_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):

    following = session.query(models.user_following).filter_by(user_id=user.id, following_id=following_id).one_or_none()
    following_user = session.query(models.User).filter_by(id=following_id).one_or_none()

    if not following_user:
        raise HTTPException(status_code=404, detail="Following user not found")
    elif not following:
        user_following = models.user_following.insert().values({"user_id": user.id, "following_id": following_id})
        session.execute(user_following)
        session.commit()

        return {
            "result": True
        }


@app.delete("/api/users/{id}/follow")
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

        return {
            "result": True
        }
    else:
        raise HTTPException(status_code=404, detail="Following not found")


@app.get("/api/tweets")
def get_tweets():
    pass


@app.get("/api/users/me")
def get_me():
    pass


@app.get("/api/users/{id}")
def get_user(user_id: int = Path(alias="id")):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True, debug=True)  # for debug
