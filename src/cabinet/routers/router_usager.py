from fastapi import APIRouter

router = APIRouter(prefix="/usager", tags=["usager"])


@router.get("/test")
async def jsp():
    return "meow"


@router.get("/")
async def get_all():
    return ""


@router.post("/")
async def create():
    return ""


@router.patch("/{id}")
async def update():
    return ""


@router.delete("/{id}")
async def delete():
    return ""


@router.get("/{id}")
async def get_one():
    return ""
