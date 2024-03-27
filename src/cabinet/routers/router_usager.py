
import mysql.connector.errors as myql_errors
from fastapi import APIRouter, HTTPException
from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.usager import UsagerUpdate,UsagerCreate
from datetime import datetime
import logging
from src.cabinet.utils.utils import change_date_format
logger = logging.getLogger("uvicorn")
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
    new_date=change_date_format(usager.date_nais)
    if new_date["error"]:
        raise HTTPException(status_code=400, detail=new_date["content"])
    usager.date_nais = new_date["content"]
    usager = dao_usager.add_usager(usager)
    return usager

@router.patch("/{id}")
async def update(id: int,usager: UsagerUpdate):
    previous_value = dao_usager.get_usager(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Usager not found")
    previous_value_dict = previous_value.__dict__

    if usager.date_nais!=None :
        new_date=change_date_format(usager.date_nais)
        if new_date["error"]:
            raise HTTPException(status_code=400, detail=new_date["content"])
        usager.date_nais = new_date["content"]

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
    """
    if (usager.sexe!='F'|usager.sexe!='H'):
        raise HTTPException(
            status_code=400,
            detail="The sexe must be F or H",
        )
    """
    
    return dao_usager.update_usager(id,usager)
   


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

 