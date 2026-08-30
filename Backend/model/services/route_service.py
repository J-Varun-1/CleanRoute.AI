from datetime import date

from data.virtual_city import (
    VIRTUAL_BINS,
    VIRTUAL_TRUCKS
)

from service.bin_status_service import (
    get_all_bin_status
)

from service.routing_service import (
    get_distance_matrix,
    optimize_route
)


def generate_route(
    prediction_date=None,
    minimum_fill=60
):

    if prediction_date is None:

        prediction_date = str(
            date.today()
        )

    bins = get_all_bin_status(
        prediction_date
    )

    # ----------------------------------
    # SELECT BINS
    # ----------------------------------

    selected_bins = [

        b for b in bins

        if b["fill_percentage"]
        >= minimum_fill
    ]

    if not selected_bins:

        return {
            "date": prediction_date,
            "message": "No bins require collection",
            "routes": []
        }

    # ----------------------------------
    # TAKE FIRST AVAILABLE TRUCK
    # ----------------------------------

    truck = next(
        (
            t for t in VIRTUAL_TRUCKS
            if t["status"] == "available"
        ),
        None
    )

    if truck is None:

        return {
            "error": "No available truck"
        }

    # ----------------------------------
    # DEPOT = TRUCK LOCATION
    # ----------------------------------

    locations = [

        (
            truck["latitude"],
            truck["longitude"]
        )
    ]

    for b in selected_bins:

        locations.append(
            (
                b["latitude"],
                b["longitude"]
            )
        )

    # ----------------------------------
    # ROAD DISTANCE MATRIX
    # ----------------------------------

    distance_matrix, duration_matrix = (
        get_distance_matrix(
            locations
        )
    )

    # ----------------------------------
    # OPTIMIZE
    # ----------------------------------

    route_indexes = optimize_route(
        distance_matrix
    )

    route_bins = []

    for index in route_indexes:

        if index == 0:

            route_bins.append({
                "type": "truck",
                "truck_id": truck["truck_id"],
                "latitude": truck["latitude"],
                "longitude": truck["longitude"]
            })

        else:

            bin_data = selected_bins[
                index - 1
            ]

            route_bins.append({
                "type": "bin",
                **bin_data
            })

    # ----------------------------------
    # TOTAL DISTANCE
    # ----------------------------------

    total_distance = 0
    total_duration = 0

    for i in range(
        len(route_indexes) - 1
    ):

        a = route_indexes[i]
        b = route_indexes[i + 1]

        total_distance += (
            distance_matrix[a][b]
        )

        total_duration += (
            duration_matrix[a][b]
        )

    return {

        "date": prediction_date,

        "truck": truck,

        "bins_selected": len(
            selected_bins
        ),

        "minimum_fill_threshold":
            minimum_fill,

        "total_distance_km":
            round(
                total_distance / 1000,
                2
            ),

        "estimated_duration_minutes":
            round(
                total_duration / 60,
                2
            ),

        "route": route_bins
    }