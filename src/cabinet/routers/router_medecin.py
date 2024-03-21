from fastapi import APIRouter

from src.cabinet.dao.dao_medecin import DaoMedecin
from src.cabinet.model.medecin import MedecinCreate, MedecinUpdate

router = APIRouter(prefix="/medecins", tags=["medecins"])
dao_medecin = DaoMedecin()


@router.get("/")
async def get_all():
    return dao_medecin.get_medecins()


@router.get("/{id}")
async def get_one(id: int):
    return dao_medecin.get_medecin(id)


@router.post("/", status_code=201)
async def create(medecin: MedecinCreate):
    medecin = dao_medecin.add_medecin(medecin)
    return medecin


@router.patch("/{id}")
async def update(id: int, medecin: MedecinUpdate):

    medecin_dict = medecin.__dict__
    given_values = medecin_dict.values()
    if not any(given_values):
        return ""

    previous_value = dao_medecin.get_medecin(id)
    if not previous_value:
        return ""
    previous_value_dict = previous_value.__dict__

    for key, value in medecin_dict.items():
        if not value:
            setattr(medecin, key, previous_value_dict[key])

    return dao_medecin.update_medecin(id, medecin)


@router.delete("/{id}")
async def delete(id: int):
    medecin = dao_medecin.get_medecin(id)
    if medecin:
        dao_medecin.delete_medecin(id)
        return medecin

    return ""
