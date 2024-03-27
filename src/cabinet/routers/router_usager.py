
import mysql.connector.errors as myql_errors
from fastapi import APIRouter, HTTPException
from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.usager import UsagerBase
from datetime import datetime

router = APIRouter(prefix="/usagers", tags=["usagers"])

dao_usager = DaoUsager()




@router.get("/")
async def get_all():
    return dao_usager.get_usagers()


@router.get("/{id}")
async def get_one(id: int):
    usager = dao_usager.get_usager(id)
    if not usager:
        raise HTTPException(status_code=404, detail="Usager not found")
    return usager

@router.post("/", status_code=201)
async def create(usager: UsagerCreate):
    usager = dao_usager.add_usager(usager)
    return usager

@router.patch("/{id}")
async def update(usager: UsagerBase):
    previous_value = dao_usager.get_usager(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Usager not found")
    previous_value_dict = previous_value.__dict__

    usager_dict = usager.__dict__
    given_values = usager_dict.values()
    if not any(given_values):
        raise HTTPException(
            status_code=400,
            detail="No values given, you must provide at least one value to update",
        )

    for key, value in usager_dict.items():
        if not value:
            setattr(usager, key, previous_value_dict[key])

    #vérifier le sexe
    if (usager.sexe!='F'|usager.sexe!='H'):
        raise HTTPException(
            status_code=400,
            detail="The sexe must be F or H",
        )
    #verifier la date
    inserted_format = "%d/%m/%Y"
    given_date = usager.date_nais
    try:
        date = datetime.strptime(given_date, inserted_format)
        usager.date_nais = date.strftime("%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="The birth date given must be in a 01/01/2000 format",
        )
    return dao_usager.add_usager(usager)
   


@router.delete("/{id}")
async def delete(id: int):
    usager = dao_usager.get_usager(id)
    if usager:
        try:
            dao_usager.delete_usager(id)
            return usager
        except myql_errors.IntegrityError as e:
            raise HTTPException(
                status_code=409,
                detail="You can't delete this usager because it is used in another table",
            )

    raise HTTPException(status_code=404, detail="usager not found")

 