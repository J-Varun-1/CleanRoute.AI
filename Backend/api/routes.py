from fastapi import APIRouter

from service.route_service import (
    generate_route
)


router = APIRouter(
    prefix="/api/routes",
    tags=["Routes"]
)


@router.get("/optimize")
def optimize_route_api(
    prediction_date: str | None = None,
    minimum_fill: float = 60
):

    return generate_route(
        prediction_date,
        minimum_fill
    )