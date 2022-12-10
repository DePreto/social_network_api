from db.session import async_session
from fastapi import Path, Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_crt_user(
        api_key: str = Header(default=None, alias="api-key"),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(models.User).filter_by(key=api_key).options(
        selectinload(models.User.following)).options(
        selectinload(models.User.followers)).options(
        selectinload(models.User.tweets)
    )
    res = await session.execute(stmt)
    user = res.scalars().one_or_none()
    print(user)
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


async def get_crt_tweet(
    tweet_id: int = Path(alias="id"),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(models.Tweet).filter_by(id=tweet_id)
    res = await session.execute(stmt)
    tweet = res.scalars().one_or_none()

    if tweet:
        return tweet
    else:
        raise HTTPException(status_code=404, detail="Tweet not found")


async def get_crt_favorite(
        tweet_id: int = Path(alias="id"),
        user: models.User = Depends(get_crt_user),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(models.Favorite).filter_by(user_id=user.id, tweet_id=tweet_id)
    res = await session.execute(stmt)
    favorite = res.scalars().one_or_none()

    if favorite:
        return favorite
    else:
        raise HTTPException(status_code=404, detail="Like not found")


async def get_user_by_id(
        user_id: int = Path(alias="id"),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(models.User).filter_by(id=user_id).options(
        selectinload(models.User.following)).options(
        selectinload(models.User.followers)).options(
        selectinload(models.User.tweets)
    )
    res = await session.execute(stmt)
    user = res.scalars().one_or_none()

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='User not found')

