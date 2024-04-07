from .connection import Connection
from ..model.consultation import (
    Consultation,
    ConsultationCreate,
    ConsultationUpdate,
    MedecinStats,
)


class DaoConsultation:
    def __init__(self):
        self.db = Connection().get_connection()

    def get_consultation(self, id_consultation) -> Consultation | None:
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM consultation WHERE id=%s",
            (id_consultation,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Consultation(*row)
        return None

    def get_consultations(self) -> list[Consultation]:
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

    def add_consultation(
        self, consultation: ConsultationCreate
    ) -> Consultation:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO consultation (date_consult, heure_consult, duree_consult, id_medecin, id_usager) VALUES (%s,"
            "%s,%s,%s,%s)",
            (
                consultation.date_consult,
                consultation.heure_consult,
                consultation.duree_consult,
                consultation.id_medecin,
                consultation.id_usager,
            ),
        )
        self.db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return self.get_consultation(last_id)

    def update_consultation(
        self, id_consultation: int, consultation: ConsultationUpdate
    ) -> Consultation:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE consultation SET date_consult=%s, heure_consult=%s, duree_consult=%s, id_medecin=%s, id_usager=%s "
            "WHERE id=%s",
            (
                consultation.date_consult,
                consultation.heure_consult,
                consultation.duree_consult,
                consultation.id_medecin,
                consultation.id_usager,
                id_consultation,
            ),
        )
        self.db.commit()
        cursor.close()
        return self.get_consultation(id_consultation)

    def delete_consultation(self, id: int) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM consultation WHERE id=%s",
            (id,),
        )
        self.db.commit()
        cursor.close()

    def get_total_duree_rdv_before_today(self) -> list[MedecinStats]:
        sql = (
            "SELECT id_medecin,ROUND(SUM(duree_consult)/60,2) AS total FROM consultation WHERE "
            "date_consult<=CURDATE() GROUP BY id_medecin"
        )

        cursor = self.db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append(MedecinStats(*row))
        return result
