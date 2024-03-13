from .connection import Connection
class DaoMedecin: 
    def __init__(self):
        self.db = Connection().get_connection()
    
    def get_medecin(self,id_medecin):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM medecin WHERE id=%s",
            (id_medecin,),
        )
        usager=cursor.fetchtone()
        cursor.close()
        return(usager)

    def get_medecins(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM medecin",
        )
        usagers=cursor.fetchall()
        cursor.close()
        return(usagers)

    def add_medecin(self,civilite,nom,prenom):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO medecin (civilite,nom,prenom) VALUES (%s,%s,%s)",
            (civilite,nom,prenom,),
        )
        self.db.commit()
        cursor.close()
    
    def update_medecin(self,id,civilite,nom,prenom):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE medecin SET civilite=%s, nom=%s, prenom=%s WHERE id=%s",
            (civilite,nom,prenom,id,),
        )
        self.db.commit()
        cursor.close()
       
    def delete_medecin(self,id):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM medecin WHERE id=%s",
            (id,),
        )
        self.db.commit()
        cursor.close()

