from pydantic import BaseModel


class Medecin:
    def __init__(self, id: int, civilite: str, nom: str, prenom: str):
        self.id = id
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom


class MedecinBase(BaseModel):
    civilite: str
    nom: str
    prenom: str
