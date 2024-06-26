import requests
from fastapi import Depends
from fastapi import FastAPI, status
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from src.cabinet.config import AUTH_URL
from src.cabinet.routers import (
    router_consultation,
    router_medecin,
    router_stats,
    router_usager,
)


def get_permissions(request: Request):
    token = request.headers.get("Authorization")
    if token:
        headers = {"Authorization": token}
        r = requests.get(AUTH_URL, headers=headers)
        if r.status_code == 200:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be logged in to access this route.",
                headers={"WWW-Authenticate": "Bearer"},
            )


description = ""
app = FastAPI(
    title="API Cabinet Medical",
    version="1.0",
    description=description,
    dependencies=[Depends(get_permissions)],
)


def cleared_loc(lst, value):
    return [x for x in lst if x != value]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    detail = exc.errors()
    modified_detail = {"status": "error", "status_code": 500}
    result = {}

    for error in detail:
        error_type = error["type"].capitalize()

        if error_type in result:
            result[error_type]["loc"].extend(error["loc"])
        else:
            result[error_type] = {
                "loc": list(error["loc"]),
                "msg": error["msg"],
            }

    for type_error in result:
        loc = result[type_error]["loc"]
        cleared = cleared_loc(loc, "body")
        result[type_error]["loc"] = cleared

    if "Missing" in result:
        modified_detail["status_code"] = 400
        modified_detail["status_message"] = (
            f"Missing {','.join(result['Missing']['loc'])}. {result['Missing']['msg']}"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(modified_detail),
        )

    if "String_type" in result:
        modified_detail["status_code"] = 400
        modified_detail["status_message"] = (
            f"Invalid {','.join(result['String_type']['loc'])}. {result['String_type']['msg']}"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(modified_detail),
        )


app.include_router(router_usager.router)
app.include_router(router_consultation.router)
app.include_router(router_medecin.router)
app.include_router(router_stats.router)
