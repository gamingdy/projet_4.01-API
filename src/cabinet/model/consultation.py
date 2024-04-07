from datetime import date, timedelta

from pydantic import BaseModel

from src.cabinet.utils.utils import sql_to_date


class Consultation:

    def __init__(
        self,
        id: int,
        date_consult: date,
        heure_consult: timedelta,
        duree_consult: int,
        id_medecin: int,
        id_usager: int,
    ):
        self.id = id
        self.date_consult = sql_to_date(date_consult)
        self.heure_consult = str(heure_consult)
        self.duree_consult = duree_consult
        self.id_medecin = id_medecin
        self.id_usager = id_usager


class ConsultationResponse(BaseModel):
    id: int
    date_consult: str
    heure_consult: str
    duree_consult: int
    id_medecin: int
    id_usager: int


class ConsultationCreate(BaseModel):
    id_usager: str
    id_medecin: str
    date_consult: str
    heure_consult: str
    duree_consult: str


class ConsultationUpdate(BaseModel):
    id_usager: str = None
    id_medecin: str = None
    date_consult: str = None
    heure_consult: str = None
    duree_consult: str = None


class MedecinStats:
    def __init__(self, id_medecin: int, total_duree: float):
        self.id_medecin = id_medecin
        self.total_duree = total_duree


class MedecinStatsResponse(BaseModel):
    id_medecin: int
    total_duree: float
