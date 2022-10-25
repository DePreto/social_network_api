from fastapi import FastAPI, Path, Body, Query, Header, Depends
from app import models, schemas
from db.session import Session
import uvicorn

app = FastAPI()


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def first_root():
    return {"Hello": "1World"}


@app.post("/api/tweets")
def post_tweet(
        tweet: schemas.TweetSchema,
        api_key: str = Header(default=None, alias="api-key"),
        session: Session = Depends(get_session)
):
    user = session.query(models.User).filter_by(key=api_key).one_or_none()

    if user:
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
def post_medias():
    pass


@app.delete("/api/tweets/{id}")
def delete_tweet(item_id: int = Path(alias="id")):
    pass


@app.post("/api/tweets/{id}/likes")
def post_like(item_id: int = Path(alias="id")):
    pass


@app.delete("/api/tweets/{id}/likes")
def delete_like(item_id: int = Path(alias="id")):
    pass


@app.post("/api/users/{id}/follow")
def post_follow(item_id: int = Path(alias="id")):
    pass


@app.delete("/api/users/{id}/follow")
def delete_follow(item_id: int = Path(alias="id")):
    pass


@app.get("/api/tweets")
def get_tweets():
    pass


@app.get("/api/users/me")
def get_me():
    pass


@app.get("/api/users/{id}")
def get_user(item_id: int = Path(alias="id")):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True, debug=True)  # for debug
