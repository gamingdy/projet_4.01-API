
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.usager import UsagerBase
from datetime import datetime

router = APIRouter(prefix="/usagers", tags=["usagers"])

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


@router.post("/",status_code=201)
async def create(usager: UsagerBase):
    #vérifier le sexe
    if (usager.sexe!='F'|usager.sexe!='H'):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid sexe value. Must be 'F' or 'H'."}
        )
    #verifier la date
    inserted_format = "%d/%m/%Y"
    given_date = usager.date_nais
    try:
        date = datetime.strptime(given_date, inserted_format)
        usager.date_nais = date.strftime("%Y-%m-%d")
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(e)}
        )
    
    usager.id_medecin=int(usager.id_medecin)

    result =dao_usager.add_usager(usager)
    return result


@router.patch("/{id}")
async def update():
    return ""


@router.delete("/{id}")
async def delete():
    return ""
 