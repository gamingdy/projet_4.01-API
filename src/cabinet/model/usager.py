from datetime import date

from pydantic import BaseModel

from src.cabinet.utils.utils import sql_to_date


class Usager:

    def __init__(
        self,
        id: int,
        civilite: str,
        nom: str,
        prenom: str,
        sexe: str,
        adresse: str,
        code_postal: str,
        ville: str,
        date_nais: date,
        lieu_nais: str,
        num_secu: str,
        id_medecin: int | None = None,
    ):
        self.id = id
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville
        self.date_nais = sql_to_date(date_nais)
        self.lieu_nais = lieu_nais
        self.num_secu = num_secu
        self.id_medecin = id_medecin


class UsagerResponse(BaseModel):
    id: int
    civilite: str
    nom: str
    prenom: str
    sexe: str
    adresse: str
    code_postal: str
    ville: str
    date_nais: str
    lieu_nais: str
    num_secu: str
    id_medecin: int | None = None


class UsagerCreate(BaseModel):
    civilite: str
    nom: str
    prenom: str
    sexe: str
    adresse: str
    code_postal: str
    ville: str
    date_nais: str
    lieu_nais: str
    num_secu: str
    id_medecin: str = None


class UsagerUpdate(BaseModel):
    civilite: str = None
    nom: str = None
    prenom: str = None
    sexe: str = None
    adresse: str = None
    code_postal: str = None
    ville: str = None
    date_nais: str = None
    lieu_nais: str = None
    num_secu: str = None
    id_medecin: str = None
