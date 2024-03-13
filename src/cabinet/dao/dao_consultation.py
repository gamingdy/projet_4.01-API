from .connection import Connection
class DaoConsultation: 
    def __init__(self):
        self.db = Connection().get_connection()
    
    def get_consultation(self,id_consultation):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM consultation WHERE id=%s",
            (id_consultation,),
        )
        usager=cursor.fetchtone()
        cursor.close()
        return(usager)

    def get_consultations(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM consultation",
        )
        usagers=cursor.fetchall()
        cursor.close()
        return(usagers)

    def add_consultation(self,date,heure,duree,medecin,usager):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO consultation (date_consult, heure_consult, duree_consult, id_medecin, id_usager) VALUES (%s,%s,%s,%s,%s)",
            (date,heure,duree,medecin,usager,),
        )
        self.db.commit()
        cursor.close()
    
    def update_consultation(self,id,date,heure,duree,medecin,usager):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE consultation SET date_consult=%s, heure_consult=%s, duree_consult=%s, id_medecin=%s, id_usager=%s WHERE id=%s",
            (date,heure,duree,medecin,usager,id,),
        )
        self.db.commit()
        cursor.close()
       
    def delete_consultation(self,id):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM consultation WHERE id=%s",
            (id,),
        )
        self.db.commit()
        cursor.close()
