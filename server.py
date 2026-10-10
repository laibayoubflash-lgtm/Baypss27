from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Baypss27 Server", version="1.0")

class DeviceData(BaseModel):
    serial_number: str

@app.get("/")
def read_root():
    return {"status": "Server is running successfully and active!"}

@app.post("/api/verify")
def verify_device(data: DeviceData):
    device_id = data.serial_number
    if not device_id:
        raise HTTPException(status_code=400, detail="Serial number is missing")
    
    return {
        "status": "success",
        "message": f"Serial number received successfully: {device_id}",
        "action": "allowed"
    }
