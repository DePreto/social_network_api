import os
import time

from fastapi import FastAPI, Path, Body, Query, Header, Depends, UploadFile, HTTPException
from app import models, schemas
from db.session import Session

import uvicorn

app = FastAPI()
out_file_path = os.environ.get("OUT_FILE_PATH")


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_crt_user(
    api_key: str = Header(default=None, alias="api-key"),
    session: Session = Depends(get_session)
):
    user = session.query(models.User).filter_by(key=api_key).one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


@app.get("/")
def first_root():
    return {"Hello": "1World"}


@app.post("/api/tweets")
def post_tweet(
        tweet: schemas.TweetSchema,
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    tweet = models.Tweet(user_id=user.id, post=tweet.tweet_data)
    session.add(tweet)
    session.flush()

    ...  # work with media

    session.commit()

    return {
        "result": True,
        "tweet_id": tweet.id
    }


@app.post("/api/medias")
def post_medias(
        file: UploadFile,
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    file_name = f"{user.id}_{time.monotonic_ns()}_{file.filename}"
    file_path = os.path.join(out_file_path, file_name)
    try:
        with open(file_path, 'wb') as out_file:
            content = file.file.read()
            out_file.write(content)
    except IOError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        media = models.Media(path=file_path)
        session.add(media)
        session.flush()

        user_media = models.UserMedia(user_id=user.id, media_id=media.id)
        session.add(user_media)
        session.commit()


@app.delete("/api/tweets/{id}")
def delete_tweet(
        tweet_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: Session = Depends(get_session)
):
    tweet = session.query(models.Tweet).filter_by(id=tweet_id, user_id=user.id).one_or_none()
    if tweet:
        session.delete(tweet)
        session.commit()

        return {
            "result": True
        }


@app.post("/api/tweets/{id}/likes")
def post_like(tweet_id: int = Path(alias="id")):
    pass


@app.delete("/api/tweets/{id}/likes")
def delete_like(tweet_id: int = Path(alias="id")):
    pass


@app.post("/api/users/{id}/follow")
def post_follow(user_id: int = Path(alias="id")):
    pass


@app.delete("/api/users/{id}/follow")
def delete_follow(user_id: int = Path(alias="id")):
    pass


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
