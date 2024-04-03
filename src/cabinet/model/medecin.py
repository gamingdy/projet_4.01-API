from pydantic import BaseModel


class Medecin:
    def __init__(self, id: int, civilite: str, nom: str, prenom: str):
        self.id = id
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom


class MedecinResponse(BaseModel):
    id: int
    civilite: str
    nom: str
    prenom: str


class MedecinCreate(BaseModel):
    civilite: str
    nom: str
    prenom: str


class MedecinUpdate(BaseModel):
    civilite: str = None
    nom: str = None
    prenom: str = None
