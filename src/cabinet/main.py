from fastapi import FastAPI

from src.cabinet.routers import (
    router_consultation,
    router_medecin,
    router_stats,
    router_usager,
)

app = FastAPI()

app.include_router(router_usager.router)
app.include_router(router_consultation.router)
app.include_router(router_medecin.router)
app.include_router(router_stats.router)
