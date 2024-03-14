from .connection import Connection
from ..model.usager import Usager


class DaoUsager:
    def __init__(self):
        self.db = Connection().get_connection()

    def get_usager(self, id_usager):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usager WHERE id = %s", (id_usager,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Usager(*row)
        return None

    def get_usagers(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usager")
        rows = cursor.fetchall()
        cursor.close()
        usagers = []
        for row in rows:
            usager = Usager(*row)
            usagers.append(usager)
        return usagers

    def add_usager(self, usager: Usager):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO usager (civilite,nom, prenom,sexe,adresse,code_postal,ville,date_nais,num_secu ) VALUES (%s, "
            "%s, %s, %s, %s, %s, %s, %s, %s,%s)",
            (
                usager.civilite,
                usager.nom,
                usager.prenom,
                usager.sexe,
                usager.adresse,
                usager.code_postal,
                usager.ville,
                usager.date_nais,
                usager.num_secu,
            ),
        )
        self.db.commit()
        cursor.close()

    def update_usager(self, usager):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE usager SET nom = %s, prenom = %s, date_naissance = %s WHERE id = %s",
            (usager.nom, usager.prenom, usager.date_naissance, usager.id),
        )
        self.db.commit()
        cursor.close()

    def delete_usager(self, usager):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM usager WHERE id = %s",
            (usager.id,),
        )
        self.db.commit()
        cursor.close()
