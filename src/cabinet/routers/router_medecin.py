from fastapi import APIRouter

from src.cabinet.dao.dao_medecin import DaoMedecin

router = APIRouter(prefix="/medecin", tags=["medecin"])
dao_medecin = DaoMedecin()


@router.get("/")
async def get_all():
    return dao_medecin.get_medecins()


@router.get("/{id}")
async def get_one(id: int):
    return dao_medecin.get_medecin(id)


@router.post("/")
async def create():
    return ""


@router.patch("/{id}")
async def update():
    return ""


@router.delete("/{id}")
async def delete():
    return ""
