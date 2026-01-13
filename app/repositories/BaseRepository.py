from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]
    db: AsyncSession

    def __init__(self, model: Type[ModelType], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID"""
        # Type checker doesn't know model has id, but BaseModel ensures it
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        # Convert Sequence to List for proper type compatibility
        return list(result.scalars().all())

    async def create(self, **kwargs: Any) -> ModelType:
        """Create a new record"""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, id: int, **kwargs: Any) -> Optional[ModelType]:
        """Update a record by ID"""
        # Type checker doesn't know model has id, but BaseModel ensures it
        await self.db.execute(
            update(self.model).where(self.model.id == id).values(**kwargs)  # type: ignore[attr-defined]
        )
        await self.db.flush()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        # Type checker doesn't know model has id, but BaseModel ensures it
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
        )
        await self.db.flush()
        # rowcount is available on CursorResult from execute()
        # Type checker doesn't recognize it, but it exists at runtime
        return bool(getattr(result, "rowcount", 0) > 0)

    async def exists(self, id: int) -> bool:
        """Check if a record exists"""
        # Type checker doesn't know model has id, but BaseModel ensures it
        result = await self.db.execute(
            select(self.model.id).where(self.model.id == id)  # type: ignore[attr-defined]
        )
        return result.scalar_one_or_none() is not None
