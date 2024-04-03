import mysql.connector.errors as myql_errors
from fastapi import APIRouter, HTTPException

from src.cabinet.dao.dao_medecin import DaoMedecin
from src.cabinet.model.medecin import (
    MedecinCreate,
    MedecinResponse,
    MedecinUpdate,
)
from src.cabinet.utils.utils import check_civilite, update_value

router = APIRouter(prefix="/medecins", tags=["medecins"])
dao_medecin = DaoMedecin()


@router.get("/", response_model=list[MedecinResponse])
async def get_all():
    return dao_medecin.get_medecins()


@router.get("/{id}", response_model=MedecinResponse)
async def get_one(id: int):
    medecin = dao_medecin.get_medecin(id)
    if not medecin:
        raise HTTPException(status_code=404, detail="Medecin not found")
    return medecin


@router.post("/", status_code=201, response_model=MedecinResponse)
async def create(medecin: MedecinCreate):
    check_civilite(medecin.civilite)
    medecin = dao_medecin.add_medecin(medecin)
    return medecin


@router.patch("/{id}", response_model=MedecinResponse)
async def update(id: int, medecin: MedecinUpdate):
    if medecin.civilite:
        check_civilite(medecin.civilite)

    previous_value = dao_medecin.get_medecin(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Medecin not found")

    update_value(previous_value, medecin)

    return dao_medecin.update_medecin(id, medecin)


@router.delete("/{id}", response_model=MedecinResponse)
async def delete(id: int):
    medecin = dao_medecin.get_medecin(id)
    if not medecin:
        raise HTTPException(status_code=404, detail="Medecin not found")

    try:
        dao_medecin.delete_medecin(id)
        return medecin
    except myql_errors.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="You can't delete this medecin because it is used in another table",
        )
