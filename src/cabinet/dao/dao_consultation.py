from .connection import Connection
from ..model.consultation import Consultation
class DaoConsultation: 
    def __init__(self):
        self.db = Connection().get_connection()
    
    def get_consultation(self,id_consultation):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM consultation WHERE id=%s",
            (id_consultation,),
        )
        row=cursor.fetchtone()
        cursor.close()
        if row:
            return Consultation(*row)
        return None

    def get_consultations(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM consultation",
        )
        rows = cursor.fetchall()
        cursor.close()
        consultations = []
        for row in rows:
            consulation = Consultation(*row)
            consultations.append(consulation)
        return consultations

    def add_consultation(self,consultation:Consultation):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO consultation (date_consult, heure_consult, duree_consult, id_medecin, id_usager) VALUES (%s,%s,%s,%s,%s)",
            (consultation.date_consult,consultation.heure_consult,consultation.duree_consult,consultation.id_medecin,consultation.id_usager,),
        )
        self.db.commit()
        cursor.close()
    
    def update_consultation(self,consultation:Consultation):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE consultation SET date_consult=%s, heure_consult=%s, duree_consult=%s, id_medecin=%s, id_usager=%s WHERE id=%s",
            (consultation.date_consult,consultation.heure_consult,consultation.duree_consult,consultation.id_medecin,consultation.id_usager,consultation.id,),
        )
        self.db.commit()
        cursor.close()
       
    def delete_consultation(self,consultation:Consultation):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM consultation WHERE id=%s",
            (consultation.id,),
        )
        self.db.commit()
        cursor.close()
