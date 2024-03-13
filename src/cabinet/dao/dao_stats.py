from .connection import Connection
from ..dao.dao_usager import DaoUsager 
from datetime import datetime
class DaoStats: 
    def __init__(self):
        self.db = Connection().get_connection()
        self.dao_usager = DaoUsager()

    def get_stat(self):
        usagers = self.dao_usager.get_usagers() 
        femme_stat = [0, 0, 0]
        homme_stat = [0, 0, 0]

        for usager in usagers:
            current_date = datetime.now()
            date_naissance = datetime.strptime(usager.date_nais, '%Y-%m-%d')
            diff = (current_date - date_naissance).days // 365 
            if diff < 25:
                age_group = 0
            elif diff < 50:
                age_group = 1
            else:
                age_group = 2

            if usager.civilite == "Mme":
                femme_stat[age_group] += 1
            else:  
                homme_stat[age_group] += 1

        return [homme_stat, femme_stat]

