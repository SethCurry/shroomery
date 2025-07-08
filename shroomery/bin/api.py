import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models.sql import Sensor
from ..models import get_db_session
from structlog import get_logger

app = FastAPI(title="Shroomery API", version="0.1.0")

class SensorListResponse(BaseModel):
    id: int
    name: str
    sensor_type: str

@app.get("/api/v1/sensors", response_model=list[SensorListResponse])
async def list_sensors(db: Session = Depends(get_db_session)):
    logger = get_logger()

    sensors = db.query(Sensor).all()
    resp = [SensorListResponse(id=sensor.id, name=sensor.name, sensor_type=sensor.sensor_type.value) for sensor in sensors]

    logger.debug("got list of sensors", num_sensors=len(resp))

    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)