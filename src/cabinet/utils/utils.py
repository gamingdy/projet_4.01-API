from datetime import datetime

from fastapi import HTTPException


def date_to_sql(given_date):

    inserted_format = "%d/%m/%Y"
    try:
        date = datetime.strptime(given_date, inserted_format)
        return {"error": False, "content": date.strftime("%Y-%m-%d")}
    except ValueError as e:
        return {
            "error": True,
            "content": "The date format is invalid. Must be 'dd/mm/yyyy'.",
        }


def sql_to_date(given_date):
    return given_date.strftime("%d/%m/%Y")


def sql_to_hour(given_hour):
    return given_hour.strftime("%H:%M")


def check_hour(heure_consult):
    try:
        datetime.strptime(heure_consult, "%H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid heure_consult value. Must be in 'hh:mm' format and valid hour.",
        )


def check_civilite(civilite):
    if civilite not in ["M", "Mme"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid civilite value. Must be 'M' or 'Mme' .",
        )


def check_sexe(sexe):
    if sexe not in ["H", "F"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sexe value. Must be 'H' or 'F' .",
        )


def check_int(value, value_name):
    if not value.isdigit():
        raise HTTPException(
            status_code=400,
            detail=f"The {value_name} must be a valid integer",
        )


def check_secu(num_secu):
    check_int(num_secu, "num_secu")
    if len(num_secu) != 15:
        raise HTTPException(
            status_code=400,
            detail="The num_secu must be a valid integer of 15 digits",
        )


def check_code_postal(code_postal):
    check_int(code_postal, "code_postal")
    if len(code_postal) != 5:
        raise HTTPException(
            status_code=400,
            detail="The code_postal must be a valid integer of 5 digits",
        )


def update_value(previous_value, new_value):
    previous_value_dict = previous_value.__dict__

    new_value_dict = new_value.__dict__
    given_values = new_value_dict.values()
    if not any(given_values):
        raise HTTPException(
            status_code=400,
            detail="No values given, you must provide at least one value to update",
        )

    for key, value in new_value_dict.items():
        if not value:
            setattr(new_value, key, previous_value_dict[key])
