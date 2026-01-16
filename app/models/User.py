from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models.BaseModel import BaseModel
import uuid as uuid_lib

if TYPE_CHECKING:
    from app.models.Role import Role


class User(BaseModel):
    __tablename__ = "users"

    # Identifiers
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(
        String, unique=True, default=lambda: str(uuid_lib.uuid4())
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column("password", String(500))

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20))
    phone_number2: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # role and status
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    # Timestamps
    email_verified_on: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_on: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
