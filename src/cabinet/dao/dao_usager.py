from .connection import Connection
from ..model.usager import UsagerBase,Usager,UsagerCreate,UsagerUpdate


class DaoUsager:
    def __init__(self):
        self.db = Connection().get_connection()

    def get_usager(self, id_usager) -> Usager | None:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usager WHERE id=%s", (id_usager,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Usager(*row)
        return None

    def get_usagers(self)-> list[Usager]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usager")
        rows = cursor.fetchall()
        cursor.close()
        usagers = []
        for row in rows:
            usager = Usager(*row)
            usagers.append(usager)
        return usagers

    def add_usager(self, usager: UsagerCreate)-> Usager | None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO usager (civilite, nom, prenom, sexe, adresse, code_postal, ville, date_nais, lieu_nais, num_secu, id_medecin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)",
            (
                usager.civilite,
                usager.nom,
                usager.prenom,
                usager.sexe,
                usager.adresse,
                usager.code_postal,
                usager.ville,
                usager.date_nais,
                usager.lieu_nais,
                usager.num_secu,
                usager.id_medecin,
            ),
        )
        self.db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return self.get_usager(last_id)

    def update_usager(self, id:int, usager:UsagerUpdate) -> Usager | None:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE usager SET civilite=%s, nom = %s, prenom = %s, date_nais = %s , sexe =%s, adresse=%s, code_postal=%s, ville=%s, lieu_nais=%s, num_secu=%s, id_medecin=%s WHERE id = %s",
            (usager.civilite,usager.nom, usager.prenom, usager.date_nais, usager.sexe,usager.adresse,usager.code_postal,usager.ville,usager.lieu_nais,usager.num_secu,usager.id_medecin,id),
        )
        self.db.commit()
        cursor.close()

    def delete_usager(self, id) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM usager WHERE id = %s",
            (id,),
        )
        self.db.commit()
        cursor.close()
