from fastapi import FastAPI

from db import Base, engine
from api.bins import router as bins_router

import models

from api.bins import router as bins_router
from api.trucks import router as trucks_router
from api.predictions import router as predictions_router
from api.routes import router as routes_router
from api.collections import router as collections_router
from api.alerts import router as alerts_router


app = FastAPI(
    title="Smart Waste Management System",
    description="AI powered smart waste collection and route optimization system for Mangaluru",
    version="1.0.0"
)


Base.metadata.create_all(
    bind=engine
)


# -------------------------
# ROUTERS
# -------------------------

from pydantic import BaseModel

from service.route_optimizer import optimize_route

from service.prediction_service import predict_bin
from service.route_optimizer import optimize_route

from data.bin_locations import BIN_LOCATIONS


app = FastAPI()



app.include_router(
    bins_router
)


app.include_router(
    trucks_router
)

app.include_router(
    predictions_router
)

app.include_router(
    routes_router
)

app.include_router(
    collections_router
)

app.include_router(
    alerts_router
)


@app.get("/")
def root():

    return {
        "project": "Smart Waste Management System",
        "city": "Mangaluru",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



ROUTE_BIN_IDS = [
    "BIN_001",
    "BIN_002",
    "BIN_003",
    "BIN_004",
    "BIN_005",
    "BIN_006",
    "BIN_007",
    "BIN_008",
    "BIN_009",
    "BIN_010"
]

class RouteRequest(BaseModel):

    date: str


@app.post("/optimize-route")
def optimize_route_api(
    request: RouteRequest
):

    date = request.date

    # ========================================================
    # CONFIGURATION
    # ========================================================

    MAX_MANDATORY_BINS = 5

    OPTIONAL_FILL_THRESHOLD = 50

    # ========================================================
    # STEP 1
    # Predict ALL 10 BINS
    # ========================================================

    predictions = []

    for bin_id in ROUTE_BIN_IDS:

        print(
            f"Predicting {bin_id}..."
        )

        prediction = predict_bin(
            bin_id,
            date
        )

        location = BIN_LOCATIONS[
            bin_id
        ]

        predictions.append({

            "bin_id": bin_id,

            "lat":
                location["lat"],

            "lon":
                location["lon"],

            "fill":
                prediction["fill"],

            "wet":
                prediction["wet"],

            "dry":
                prediction["dry"]

        })

    # ========================================================
    # STEP 2
    # Sort ONLY for selecting priority bins
    # ========================================================

    ranked_bins = sorted(
        predictions,
        key=lambda x: x["fill"],
        reverse=True
    )

    # ========================================================
    # STEP 3
    # TOP 5 = MANDATORY
    # ========================================================

    mandatory_bins = ranked_bins[
        :MAX_MANDATORY_BINS
    ]

    mandatory_ids = {
        bin_data["bin_id"]
        for bin_data in mandatory_bins
    }

    # ========================================================
    # STEP 4
    # Remaining bins = candidates
    # ========================================================

    optional_bins = [

        bin_data

        for bin_data in predictions

        if (
            bin_data["bin_id"]
            not in mandatory_ids
        )

        and

        (
            bin_data["fill"]
            >= OPTIONAL_FILL_THRESHOLD
        )
    ]

    # ========================================================
    # DEBUG
    # ========================================================

    print("\n======================================")
    print("MANDATORY BINS")
    print("======================================")

    for bin_data in mandatory_bins:

        print(
            bin_data["bin_id"],
            "→",
            round(
                bin_data["fill"],
                2
            ),
            "%"
        )

    print("\n======================================")
    print("OPTIONAL BINS")
    print("======================================")

    for bin_data in optional_bins:

        print(
            bin_data["bin_id"],
            "→",
            round(
                bin_data["fill"],
                2
            ),
            "%"
        )

    # ========================================================
    # STEP 5
    # DEPOT
    # ========================================================

    depot = (
        19.0750,
        72.8770
    )

    # ========================================================
    # STEP 6
    # OR-TOOLS
    # ========================================================

    optimized_route = optimize_route(

        mandatory_bins,

        optional_bins,

        depot

    )

    # ========================================================
    # STEP 7
    # RETURN
    # ========================================================

    return {

        "status": "success",

        "date": date,

        "total_bins_checked":
            len(predictions),

        "mandatory_bins":
            mandatory_bins,

        "optional_candidates":
            optional_bins,

        "optimized_route":
            optimized_route

    }