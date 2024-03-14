from datetime import date, time


class Consultation:

    def __init__(
        self,
        id: int,
        date_consult: date,
        heure_consult: time,
        duree_consult: int,
        id_medecin: int,
        id_usager: int,
    ):
        self.id = id
        self.date_consult = date_consult  # Using date type
        self.heure_consult = heure_consult  # Using time type
        self.duree_consult = duree_consult
        self.id_medecin = id_medecin
        self.id_usager = id_usager
