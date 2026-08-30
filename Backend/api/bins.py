from fastapi import APIRouter, Query
from datetime import date

from data.virtual_city import VIRTUAL_BINS
from service.bin_status_service import get_all_bin_status


router = APIRouter(
    prefix="/api/bins",
    tags=["Bins"]
)


@router.get("/")
def get_bins(
    prediction_date: str | None = Query(
        default=None
    )
):

    if prediction_date is None:

        prediction_date = str(
            date.today()
        )

    return {
        "date": prediction_date,
        "total_bins": len(VIRTUAL_BINS),
        "bins": get_all_bin_status(
            prediction_date
        )
    }


@router.get("/{bin_id}")
def get_bin(
    bin_id: str,
    prediction_date: str | None = None
):

    if prediction_date is None:

        prediction_date = str(
            date.today()
        )

    for bin_data in VIRTUAL_BINS:

        if bin_data["bin_id"] == bin_id:

            from service.bin_status_service import (
                get_bin_status
            )

            return get_bin_status(
                bin_data,
                prediction_date
            )

    return {
        "error": "Bin not found"
    }