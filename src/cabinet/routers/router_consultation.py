from fastapi import APIRouter, HTTPException

from src.cabinet.dao.dao_consultation import DaoConsultation
from src.cabinet.dao.dao_medecin import DaoMedecin
from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.consultation import (
    ConsultationCreate,
    ConsultationResponse,
    ConsultationUpdate,
)
from src.cabinet.utils.utils import check_hour, date_to_sql, update_value

router = APIRouter(prefix="/consultations", tags=["consultations"])
dao_consultation = DaoConsultation()
dao_usager = DaoUsager()
dao_medecin = DaoMedecin()


@router.get("/", response_model=list[ConsultationResponse])
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

    usager = dao_usager.get_usager(consultation.id_usager)
    if not usager:
        raise HTTPException(status_code=404, detail="Usager not found")

    medecin = dao_medecin.get_medecin(consultation.id_medecin)
    if not medecin:
        raise HTTPException(status_code=404, detail="Medecin not found")

    new_date = date_to_sql(consultation.date_consult)
    if new_date["error"]:
        raise HTTPException(status_code=400, detail=new_date["content"])

    consultation.date_consult = new_date["content"]

    check_hour(consultation.heure_consult)

    consultation = dao_consultation.add_consultation(consultation)

    return consultation


@router.patch("/{id}", response_model=ConsultationResponse)
async def update(id: int, consultation: ConsultationUpdate):

    previous_value = dao_consultation.get_consultation(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Consultation not found")

    if consultation.date_consult is not None:
        new_date = date_to_sql(consultation.date_consult)
        if new_date["error"]:
            raise HTTPException(status_code=400, detail=new_date["content"])
        consultation.date_consult = new_date["content"]

    if consultation.heure_consult is not None:
        check_hour(consultation.heure_consult)

    update_value(previous_value, consultation)

    return dao_consultation.update_consultation(id, consultation)


@router.delete("/{id}", response_model=ConsultationResponse)
async def delete(id: int):
    consultation = dao_consultation.get_consultation(id)
    if consultation:
        dao_consultation.delete_consultation(id)
        return consultation
