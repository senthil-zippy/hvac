from fastapi import FastAPI

from routers import buildings, floors, portfolios, zones

app = FastAPI(title="ZoneIQ Portfolio API")

app.include_router(portfolios.router)
app.include_router(buildings.router)
app.include_router(floors.router)
app.include_router(zones.router)


@app.get("/health")
def health():
    return {"status": "ok"}
