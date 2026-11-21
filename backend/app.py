"""Local API skeleton; no forecast or clinical inference is performed."""
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="AERIVA Core API", version="0.1.0", description="Local draft; forecast and auth not implemented.")


def validate_window(start: datetime, end: datetime) -> None:
    if start.utcoffset() is None or end.utcoffset() is None:
        raise HTTPException(400, "start dan end harus menyertakan zona waktu atau offset")
    if start >= end:
        raise HTTPException(400, "start harus lebih awal daripada end")


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "forecast_provider_configured": False}


@app.get("/api/v1/environment/assessment")
def assessment(lat: Annotated[float, Query(ge=-90, le=90)], lon: Annotated[float, Query(ge=-180, le=180)], start: datetime, end: datetime):
    validate_window(start, end)
    return {"location": {"lat": lat, "lon": lon}, "window": {"start": start, "end": end}, "data_status": "unavailable", "periods": [], "message": "Sumber prakiraan belum terhubung."}


@app.get("/api/v1/environment/recommendations")
def recommendations(lat: Annotated[float, Query(ge=-90, le=90)], lon: Annotated[float, Query(ge=-180, le=180)], start: datetime, end: datetime):
    validate_window(start, end)
    return {"location": {"lat": lat, "lon": lon}, "window": {"start": start, "end": end}, "status": "insufficient_data", "recommended_period": None, "reasons": [], "message": "Data prakiraan dan aturan penilaian belum tersedia."}
