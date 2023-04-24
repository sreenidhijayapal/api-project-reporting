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

@app.get("/lookup/{ip_address}")
async def lookup(ip_address: str):
    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch geolocation data")
    geolocation_data = json.loads(response.text)

    response = requests.get(f"https://www.abuseipdb.com/check/{ip_address}/json?key=<YOUR_API_KEY>&days=30")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch abuse data")
    abuse_data = json.loads(response.text)

    data = {
        "id": "1",
        "ipAddress": ip_address,
        "location": {
            "country": geolocation_data["country"],
            "region": geolocation_data["regionName"],
            "city": geolocation_data["city"],
            "lat": geolocation_data["lat"],
            "lng": geolocation_data["lon"],
            "postalCode": geolocation_data["zip"],
            "timezone": geolocation_data["timezone"]
        },
        "domains": [],
        "as": {
            "asn": geolocation_data["as"],
            "name": geolocation_data["isp"],
            "route": "",
            "domain": geolocation_data["org"]
        },
        "isp": geolocation_data["isp"]
    }

    for domain in abuse_data["data"]["domains"]:
        data["domains"].append(domain["domain"])

    data["as"]["route"] = abuse_data["data"]["ipAddressDetails"]["route"]

    return data
