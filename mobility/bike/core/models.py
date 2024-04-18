import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    DECIMAL,
    UUID,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Time,
    func,
)
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
    external_id: Mapped[int] = mapped_column(Integer, nullable=True)
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


class Bike(db.Model):
    __tablename__ = "bike"
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    code: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="AVAILABLE")
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    last_lat: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    last_lon: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )

    trips = relationship("Trip", back_populates="bike")


class Trip(db.Model):
    __tablename__ = "trip"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    user_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.uuid"))
    bike_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bike.uuid"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    start_lat: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    start_lon: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    end_lat: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    end_lon: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=9, scale=6), nullable=True
    )
    time_used: Mapped[time] = mapped_column(Time, nullable=True)
    fare: Mapped[float] = mapped_column(Float, nullable=True)
    payment_method_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("payment_method.id")
    )
    with_subscription: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False
    )
    calorie: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )

    user = relationship("User", back_populates="trips")
    bike = relationship("Bike", back_populates="trips")
    payment_method = relationship("PaymentMethod", back_populates="trips")


class Country(db.Model):
    __tablename__ = "country"

    code: Mapped[str] = mapped_column(
        String(length=2), unique=True, index=True, primary_key=True
    )  # ISO-3166
    name: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String, nullable=True)
    currency: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    locale: Mapped[str] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="country")


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"

    id: Mapped[UUID] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    trips = relationship("Trip", back_populates="payment_method")
