from fastapi import APIRouter


from ..services.ai_service import (
    generate_reading
)


router = APIRouter()



# =========================
# AI test endpoint
# =========================

@router.post("/ai/test")
def test_ai():


    result = generate_reading(

        "Artificial Intelligence",

        "B2",

        []

    )


    return result