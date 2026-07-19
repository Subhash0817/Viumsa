from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "application": "Viumsa",
        "version": "0.1.0",
        "status": "running"
    }