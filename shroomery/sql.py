from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    Enum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass


class SensorType(enum.Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    CO2 = "co2"
    LIGHT = "light"


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sensor_type: Mapped[SensorType] = mapped_column(Enum(SensorType), nullable=False)
    
    readings: Mapped[list["SensorReading"]] = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensors.id"), nullable=False
    )
    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="readings")
    reading_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reading_value: Mapped[float] = mapped_column(Float, nullable=False)


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    min_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    max_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    min_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    max_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
