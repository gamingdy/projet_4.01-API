from fastapi import APIRouter

from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.usager import UsagerBase

router = APIRouter(prefix="/usager", tags=["usager"])

dao_usager = DaoUsager()


@router.get("/test")
async def jsp():
    return "meow"


@router.get("/")
async def get_all():
    return dao_usager.get_usagers()


@router.get("/{id}")
async def get_one(id: int):
    return dao_usager.get_usager(id)


@router.post("/")
async def create(usager: UsagerBase):
    return usager


@router.patch("/{id}")
async def update():
    return ""


@router.delete("/{id}")
async def delete():
    return ""
 