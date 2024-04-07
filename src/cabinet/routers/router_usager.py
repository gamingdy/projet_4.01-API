import logging

import mysql.connector.errors as myql_errors
from fastapi import APIRouter, HTTPException

from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.usager import UsagerCreate, UsagerResponse, UsagerUpdate
from src.cabinet.utils.utils import (
    check_civilite,
    check_code_postal,
    check_int,
    check_secu,
    check_sexe,
    date_to_sql,
    update_value,
)

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/usagers", tags=["usagers"])

dao_usager = DaoUsager()


@router.get("/", response_model=list[UsagerResponse])
async def get_all():
    return dao_usager.get_usagers()


@router.get("/{id}", response_model=UsagerResponse)
async def get_one(id: int):
    usager = dao_usager.get_usager(id)
    if not usager:
        raise HTTPException(status_code=404, detail="Usager not found")
    return usager


@router.post("/", status_code=201, response_model=UsagerResponse)
async def create(usager: UsagerCreate):

    check_civilite(usager.civilite)
    check_sexe(usager.sexe)

    check_int(usager.id_medecin, "id_medecin")
    check_secu(usager.num_secu)
    check_code_postal(usager.code_postal)

    new_date = date_to_sql(usager.date_nais)
    if new_date["error"]:
        raise HTTPException(status_code=400, detail=new_date["content"])

    usager.date_nais = new_date["content"]
    return dao_usager.add_usager(usager)


@router.patch("/{id}", response_model=UsagerResponse)
async def update(id: int, usager: UsagerUpdate):
    if usager.date_nais is not None:
        new_date = date_to_sql(usager.date_nais)
        if new_date["error"]:
            raise HTTPException(status_code=400, detail=new_date["content"])
        usager.date_nais = new_date["content"]

    if usager.civilite is not None:
        check_civilite(usager.civilite)

    if usager.sexe is not None:
        check_sexe(usager.sexe)

    if usager.num_secu is not None:
        check_secu(usager.num_secu)

    if usager.id_medecin is not None:
        check_int(usager.id_medecin, "id_medecin")

    if usager.code_postal is not None:
        check_code_postal(usager.code_postal)

    previous_value = dao_usager.get_usager(id)
    if not previous_value:
        raise HTTPException(status_code=404, detail="Usager not found")

    update_value(previous_value, usager)

    return dao_usager.update_usager(id, usager)


@router.delete("/{id}", response_model=UsagerResponse)
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
