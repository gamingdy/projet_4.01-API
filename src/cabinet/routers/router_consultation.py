from fastapi import APIRouter

from src.cabinet.dao.dao_consultation import DaoConsultation

router = APIRouter(prefix="/consultation", tags=["consultation"])
dao_consultation = DaoConsultation()


@router.get("/")
async def get_all():
    return dao_consultation.get_consultations()


@router.get("/{id}")
async def get_one(id: int):
    return dao_consultation.get_consultation(id)


@router.post("/")
async def create():
    return ""


@router.patch("/{id}")
async def update():
    return ""


@router.delete("/{id}")
async def delete():
    return ""
