class Usager:
    id: int
    civilite: str
    nom: str
    prenom: str
    sexe: str
    adresse: str
    code_postal: int
    ville: str
    date_nais: str
    num_secu: int
    
    def __init__(self, id: int, civilite: str, nom: str, prenom: str, sexe: str, adresse: str, code_postal: int, ville: str, date_nais: str, num_secu: int):
        self.id = id
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville
        self.date_nais = date_nais
        self.num_secu = num_secu

