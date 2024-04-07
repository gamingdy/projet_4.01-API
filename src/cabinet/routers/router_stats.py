from datetime import datetime

from fastapi import APIRouter

from src.cabinet.dao.dao_consultation import DaoConsultation
from src.cabinet.dao.dao_usager import DaoUsager
from src.cabinet.model.consultation import MedecinStatsResponse

router = APIRouter(prefix="/stats", tags=["stats"])
dao_usager = DaoUsager()
dao_consultation = DaoConsultation()


def get_stat():
    usagers = dao_usager.get_usagers()
    sexe_repartition = {
        "H": {"< 25": 0, "25 - 50": 0, "> 50": 0},
        "F": {"< 25": 0, "25 - 50": 0, "> 50": 0},
    }

    for usager in usagers:
        current_date = datetime.now()
        date_naissance = datetime.strptime(usager.date_nais, "%d/%m/%Y")
        diff = (current_date - date_naissance).days // 365
        if diff < 25:
            age_group = "< 25"
        elif diff < 50:
            age_group = "25 - 50"
        else:
            age_group = "> 50"

        sexe_repartition[usager.sexe][age_group] += 1

    return sexe_repartition


@router.get("/medecins", response_model=list[MedecinStatsResponse])
async def stats_medecin():
    return dao_consultation.get_total_duree_rdv_before_today()


@router.get("/usagers", responses={200: {"model": dict[str, dict[str, int]]}})
async def stats_usager():
    return get_stat()
