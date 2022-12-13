import os
import json

from aiofiles import open as async_open
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.depends import get_crt_user, get_session, get_crt_tweet, get_crt_favorite, get_user_by_id
from app.config import settings
from app.utils import get_rnd_file_name_by_content_type
from app import schemas
from app import models


router = APIRouter()


@router.post("/api/tweets", response_model=schemas.PostTweetResponseSchema, status_code=201, tags=["tweets"])
async def post_tweet(
        data: schemas.PostTweetSchema,
        user: models.User = Depends(get_crt_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по отправке твита.
    """

    tweet = models.Tweet(user_id=user.id, post=data.tweet_data)
    session.add(tweet)
    await session.flush()

    for media_id in data.tweet_media_ids:
        stmt = select(models.Media).filter_by(id=media_id)
        result = await session.execute(stmt, execution_options={"populate_existing": True})
        media = result.scalars().one_or_none()
        if not media:
            raise HTTPException(status_code=404, detail=f"media {media_id} not found")

        post_media = models.tweet_media.insert().values({"tweet_id": tweet.id, "media_id": media_id})
        await session.execute(post_media)

    await session.commit()

    return {
        "result": True,
        "tweet_id": tweet.id
    }


@router.post("/api/medias", response_model=schemas.PostMediaResponseSchema, status_code=201, tags=["medias"])
async def post_medias(
        file: UploadFile,
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по загрузки медиа.
    """

    file_name = get_rnd_file_name_by_content_type(file.content_type)
    file_path = os.path.join(settings.OUT_FILE_PATH, file_name)
    try:
        async with async_open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except IOError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    else:
        media = models.Media(path=file_path)
        session.add(media)

    await session.commit()

    return {
        "result": True,
        "media_id": media.id,
    }


@router.delete("/api/tweets/{id}", response_model=schemas.DefaultSuccessSchema, tags=["tweets"])
async def delete_tweet(
        user: models.User = Depends(get_crt_user),
        tweet: models.Tweet = Depends(get_crt_tweet),
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по удалению твита.
    """

    if user.id == tweet.user_id:
        await session.delete(tweet)
        await session.commit()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/api/tweets/{id}/likes", response_model=schemas.DefaultSuccessSchema, status_code=201, tags=["likes"])
async def post_like(
        tweet: models.Tweet = Depends(get_crt_tweet),
        user: models.User = Depends(get_crt_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по добавлению отметки "нравится".
    """

    stmt = select(models.Favorite).filter_by(user_id=user.id, tweet_id=tweet.id)
    result = await session.execute(stmt)
    favourite_exist = result.scalars().one_or_none()

    if favourite_exist:
        raise HTTPException(status_code=409, detail="Favourite already exists.")
    else:
        favourite = models.Favorite(user_id=user.id, tweet_id=tweet.id)
        session.add(favourite)
        await session.commit()


@router.delete("/api/tweets/{id}/likes", response_model=schemas.DefaultSuccessSchema, tags=["likes"])
async def delete_like(
        favourite: models.Favorite = Depends(get_crt_favorite),
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по удалению отметки "Нравится".
    """

    await session.delete(favourite)
    await session.commit()


@router.post("/api/users/{id}/follow", response_model=schemas.DefaultSuccessSchema, status_code=201, tags=["follow"])
async def post_follow(
        following_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint по созданию подписки на пользователя.
    """

    user_stmt = select(models.User).filter_by(id=following_id)
    following_stmt = select(models.user_following).filter_by(user_id=user.id, following_id=following_id)

    user_res = await session.execute(user_stmt)
    following_res = await session.execute(following_stmt)
    following_user = user_res.scalars().one_or_none()
    following = following_res.scalars().one_or_none()

    if not following_user:
        raise HTTPException(status_code=404, detail="Following user not found")
    elif following_id == user.id:
        raise HTTPException(status_code=409, detail="User can't follow himself.")
    elif following:
        raise HTTPException(status_code=409, detail="Following already exists.")
    else:
        user_following = models.user_following.insert().values({"user_id": user.id, "following_id": following_id})
        await session.execute(user_following)
        await session.commit()


@router.delete("/api/users/{id}/follow", response_model=schemas.DefaultSuccessSchema, tags=["follow"])
async def delete_follow(
        following_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Endoint по удалению подписки с пользователя.
    """

    stmt = select(models.user_following).filter_by(user_id=user.id, following_id=following_id)
    res = await session.execute(stmt)
    following = res.scalars().one_or_none()

    if following:
        delete_stmt = delete(models.user_following).where(
            models.user_following.c.user_id == user.id,
            models.user_following.c.following_id == following_id
        )

        await session.execute(delete_stmt)
        await session.commit()

    else:
        raise HTTPException(status_code=404, detail="Following not found")


@router.get("/api/tweets", response_model=schemas.FeedSchemaOut, tags=["tweets"])
async def get_tweets(
        user: models.User = Depends(get_crt_user),
):
    """
    Endpoint по генерации ленты с твитами в соответствии с подписками пользователя.
    """

    feed = []
    for flw_user in user.following:
        feed.extend(flw_user.tweets)
    feed.sort(key=lambda x: x.created_at, reverse=True)

    return {
        "result": True,
        "tweets": [json.loads(schemas.TweetSchemaIn.from_orm(tweet).json(models_as_dict=False)) for tweet in feed],
    }


@router.get("/api/users/me", response_model=schemas.PageSchema, tags=["users"])
async def get_me(
        user: models.User = Depends(get_crt_user)
):
    """
    Endpoint с информацией о профиле текущего пользователя.
    """

    return {
        "result": True,
        "user": schemas.UserSchema.from_orm(user).dict(by_alias=True)
    }


@router.get("/api/users/{id}", response_model=schemas.PageSchema, tags=["users"])
async def get_user(
        user: models.User = Depends(get_user_by_id)
):
    """
    Endpoint с информацией о профиле заданного пользователя.
    """

    return {
        "result": True,
        "user": schemas.UserSchema.from_orm(user).dict(by_alias=True)
    }
