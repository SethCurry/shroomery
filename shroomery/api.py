from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .sql import Sensor
from .database import get_db

app = FastAPI(title="Shroomery API", version="0.1.0")

class SensorListResponse(BaseModel):
    id: int
    name: str
    sensor_type: str

@app.get("/api/v1/sensors", response_model=list[SensorListResponse])
async def list_sensors(db: Session = Depends(get_db)):
    sensors = db.query(Sensor).all()
    return [SensorListResponse(id=sensor.id, name=sensor.name, sensor_type=sensor.sensor_type.value) for sensor in sensors]