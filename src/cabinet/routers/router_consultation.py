from typing import List

from fastapi import APIRouter, HTTPException

from src.cabinet.dao.dao_consultation import DaoConsultation
from src.cabinet.model.consultation import (
    ConsultationCreate,
    ConsultationResponse,
    ConsultationUpdate,
)
from src.cabinet.utils.utils import check_hour, date_to_sql, update_value

router = APIRouter(prefix="/consultations", tags=["consultations"])
dao_consultation = DaoConsultation()


@router.get("/", response_model=List[ConsultationResponse])
async def get_all():
    return dao_consultation.get_consultations()


@router.get("/{id}", response_model=ConsultationResponse)
async def get_one(id: int):
    consultation = dao_consultation.get_consultation(id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation


@router.post("/", status_code=201, response_model=ConsultationResponse)
async def create(consultation: ConsultationCreate):
    if (
        not consultation.id_usager.isdigit()
        or not consultation.id_medecin.isdigit()
    ):
        raise HTTPException(
            status_code=400, detail="Invalid id value. Must be an integer."
        )

    if not consultation.duree_consult.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid duree_consult value. Must be an integer.",
        )

    new_date = date_to_sql(consultation.date_consult)
    if new_date["error"]:
        raise HTTPException(status_code=400, detail=new_date["content"])

    consultation.date_consult = new_date["content"]

    if not check_hour(consultation.heure_consult):
        raise HTTPException(
            status_code=400,
            detail="Invalid heure_consult value. Must be in 'hh:mm' format.",
        )

    consultation = dao_consultation.add_consultation(consultation)

    return consultation


@router.patch("/{id}", response_model=ConsultationResponse)
async def update(id: int, consultaion: ConsultationUpdate):

    previous_value = dao_consultation.get_consultation(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Consultation not found")

    if consultaion.date_consult is not None:
        new_date = date_to_sql(consultaion.date_consult)
        if new_date["error"]:
            raise HTTPException(status_code=400, detail=new_date["content"])
        consultaion.date_consult = new_date["content"]

    if consultaion.heure_consult is not None:
        if not check_hour(consultaion.heure_consult):
            raise HTTPException(
                status_code=400,
                detail="Invalid heure_consult value. Must be in 'hh:mm' format and valid hour.",
            )

    update_value(previous_value, consultaion)

    return dao_consultation.update_consultation(id, consultaion)


@router.delete("/{id}", response_model=ConsultationResponse)
async def delete(id: int):
    consultation = dao_consultation.get_consultation(id)
    if consultation:
        dao_consultation.delete_consultation(id)
        return consultation
