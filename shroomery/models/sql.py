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

class Pin(Base):
    __tablename__ = "pins"

    pin_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensors.id"))
    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="pins")

class SensorType(enum.Enum):
    SHT45 = "sht45"


class Sensor(Base):
    __tablename__ = "sensors"

    # The unique ID of the sensor
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # The name of the sensor
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # The type of the sensor
    sensor_type: Mapped[SensorType] = mapped_column(Enum(SensorType), nullable=False)

    # The pins associated with the sensor
    pins: Mapped[list["Pin"]] = relationship("Pin", back_populates="sensor")

    # The readings associated with the sensor
    readings: Mapped[list["SensorReading"]] = relationship("SensorReading", back_populates="sensor")


class SensorReadingType(enum.Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    reading_type: Mapped[SensorReadingType] = mapped_column(Enum(SensorReadingType), nullable=False, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensors.id"), nullable=False, primary_key=True
    )
    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="readings")
    reading_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, primary_key=True)
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
