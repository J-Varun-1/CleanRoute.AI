from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel

from service.prediction_service import (
    generate_prediction
)

from service.bin_metadata import (
    BIN_METADATA
)


router = APIRouter(
    prefix="/api/predictions",
    tags=["Predictions"]
)


# =========================================================
# REQUEST
# =========================================================

class PredictionRequest(BaseModel):

    bin_id: str

    date: str


# =========================================================
# PREDICTION
# =========================================================

@router.post("/predict")
def predict_bin(
    request: PredictionRequest
):

    # -----------------------------------------------------
    # BIN CHECK
    # -----------------------------------------------------

    if request.bin_id not in BIN_METADATA:

        raise HTTPException(
            status_code=404,
            detail="Bin not found"
        )


    # -----------------------------------------------------
    # ML
    # -----------------------------------------------------

    try:

        prediction = (
            generate_prediction(
                request.bin_id,
                request.date
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    metadata = BIN_METADATA[
        request.bin_id
    ]


    return {

        "bin_id":
            request.bin_id,

        "date":
            request.date,

        "area_type":
            metadata["area_type"],

        "prediction":
            prediction
    }