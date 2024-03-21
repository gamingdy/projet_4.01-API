import mysql.connector.errors as myql_errors
from fastapi import APIRouter, HTTPException

from src.cabinet.dao.dao_medecin import DaoMedecin
from src.cabinet.model.medecin import MedecinCreate, MedecinUpdate

router = APIRouter(prefix="/medecins", tags=["medecins"])
dao_medecin = DaoMedecin()


@router.get("/")
async def get_all():
    return dao_medecin.get_medecins()


@router.get("/{id}")
async def get_one(id: int):
    medecin = dao_medecin.get_medecin(id)
    if not medecin:
        raise HTTPException(status_code=404, detail="Medecin not found")
    return medecin


@router.post("/", status_code=201)
async def create(medecin: MedecinCreate):
    medecin = dao_medecin.add_medecin(medecin)
    return medecin


@router.patch("/{id}")
async def update(id: int, medecin: MedecinUpdate):

    previous_value = dao_medecin.get_medecin(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Medecin not found")
    previous_value_dict = previous_value.__dict__

    medecin_dict = medecin.__dict__
    given_values = medecin_dict.values()
    if not any(given_values):
        raise HTTPException(
            status_code=400,
            detail="No values given, you must provide at least one value to update",
        )

    for key, value in medecin_dict.items():
        if not value:
            setattr(medecin, key, previous_value_dict[key])

    return dao_medecin.update_medecin(id, medecin)


@router.delete("/{id}")
async def delete(id: int):
    medecin = dao_medecin.get_medecin(id)
    if medecin:
        try:
            dao_medecin.delete_medecin(id)
            return medecin
        except myql_errors.IntegrityError as e:
            raise HTTPException(
                status_code=409,
                detail="You can't delete this medecin because it is used in another table",
            )

    raise HTTPException(status_code=404, detail="Medecin not found")
