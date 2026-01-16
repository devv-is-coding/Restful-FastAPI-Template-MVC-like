from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.User import User
from app.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def create(self, **kwargs) -> User:
        """Create a new user with role eager loaded"""
        user = User(**kwargs)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user, ["role"])  # Eagerly load the role
        return user

    async def get_by_id(self, id: int) -> Optional[User]:
        """Get user by ID with role loaded"""
        result = await self.db.execute(
            select(User).options(selectinload(User.role)).where(User.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).options(selectinload(User.role)).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with roles loaded"""
        result = await self.db.execute(
            select(User).options(selectinload(User.role)).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, id: int, **kwargs) -> Optional[User]:
        """Update user and return with role loaded"""
        user = await self.get_by_id(id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.db.flush()
            await self.db.refresh(user, ["role"])
        return user

    async def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        result = await self.db.execute(select(User.id).where(User.email == email))
        return result.scalar_one_or_none() is not None

    async def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        result = await self.db.execute(select(User.id).where(User.username == username))
        return result.scalar_one_or_none() is not None
