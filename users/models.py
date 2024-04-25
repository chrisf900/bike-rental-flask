import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import UUID, Date, DateTime, ForeignKey, Identity, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db


class User(db.Model):
    __tablename__ = "user"
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    external_id: Mapped[int] = mapped_column(Integer, Identity(start=1000))
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    gender_id: Mapped[int] = mapped_column(Integer, ForeignKey("gender.id"))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=True)
    country_code: Mapped[str] = mapped_column(String, ForeignKey("country.code"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )

    country = relationship("Country", back_populates="user")
    gender = relationship("Gender", back_populates="user")
    trips = relationship("Trip", back_populates="user")


class Gender(db.Model):
    __tablename__ = "gender"

    id: Mapped[UUID] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    user = relationship("User", back_populates="gender")


class PasswordHistory(db.Model):
    __tablename__ = "password_history"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    user_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.uuid"))
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User")
