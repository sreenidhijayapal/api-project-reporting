from fastapi import FastAPI, HTTPException
from typing import Optional
import requests
import json

app = FastAPI()

@app.get("/geolocation/{ip_address}")
async def geolocation(ip_address: str):
    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch geolocation data")
    data = json.loads(response.text)
    return data

@app.get("/abuse/{ip_address}")
async def abuse(ip_address: str, days: Optional[int] = 30):
    response = requests.get(f"https://www.abuseipdb.com/check/{ip_address}/json?key=<YOUR_API_KEY>&days={days}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch abuse data")
    data = json.loads(response.text)
    return data
