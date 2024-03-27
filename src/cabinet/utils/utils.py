from datetime import datetime


def change_date_format(given_date):

    inserted_format = "%d/%m/%Y"
    try:
        date = datetime.strptime(given_date, inserted_format)
        return {"error": False, "content": date.strftime("%Y-%m-%d")}
    except ValueError as e:
        return {
            "error": True,
            "content": "The date format is invalid. Must be 'dd/mm/yyyy'.",
        }


def check_hour(heure_consult):
    try:
        datetime.strptime(heure_consult, "%H:%M")
        return True
    except ValueError:
        return False
