from fastapi import APIRouter

router = APIRouter(prefix="/medecin", tags=["medecin"])


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
