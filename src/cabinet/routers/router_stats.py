from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/medecin")
async def stats_medecin():
    return ""


@router.get("/usager")
async def stats_usager():
    return ""
