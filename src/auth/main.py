from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic
from passlib.context import CryptContext

from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.dao.login import DaoLogin
from src.auth.model.token import Token
from src.auth.model.user import User
from src.auth.utils.funct import create_access_token, get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


app = FastAPI()


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


@app.post("/")
async def login(form_data: User) -> Token:
    dao_login = DaoLogin()
    user = dao_login.login(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
