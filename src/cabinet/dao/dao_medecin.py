from .connection import Connection
from ..model.medecin import Medecin


class DaoMedecin:
    def __init__(self):
        self.db = Connection().get_connection()

    def get_medecin(self, id_medecin):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM medecin WHERE id=%s",
            (id_medecin,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Medecin(*row)
        return None

    def get_medecins(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM medecin",
        )
        rows = cursor.fetchall()
        cursor.close()
        medecins = []
        for row in rows:
            medecin = Medecin(*row)
            medecins.append(medecin)
        return medecins

    def add_medecin(self, medecin: Medecin):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO medecin (civilite,nom,prenom) VALUES (%s,%s,%s)",
            (
                medecin.civilite,
                medecin.nom,
                medecin.prenom,
            ),
        )
        self.db.commit()
        cursor.close()

    def update_medecin(self, medecin: Medecin):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE medecin SET civilite=%s, nom=%s, prenom=%s WHERE id=%s",
            (
                medecin.civilite,
                medecin.nom,
                medecin.prenom,
                medecin.id,
            ),
        )
        self.db.commit()
        cursor.close()

    def delete_medecin(self, medecin: Medecin):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM medecin WHERE id=%s",
            (medecin.id,),
        )
        self.db.commit()
        cursor.close()
