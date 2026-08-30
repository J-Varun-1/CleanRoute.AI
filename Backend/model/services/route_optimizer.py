from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

import math


# ============================================================
# DISTANCE
# ============================================================

def calculate_distance(point1, point2):

    lat1, lon1 = point1
    lat2, lon2 = point2

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )


# ============================================================
# DISTANCE MATRIX
# ============================================================

def build_distance_matrix(locations):

    matrix = []

    for i in range(len(locations)):

        row = []

        for j in range(len(locations)):

            distance = calculate_distance(
                locations[i],
                locations[j]
            )

            row.append(
                int(distance * 100000)
            )

        matrix.append(row)

    return matrix


# ============================================================
# OPTIMIZE ROUTE
# ============================================================

def optimize_route(
    mandatory_bins,
    optional_bins,
    depot
):

    # --------------------------------------------------------
    # IMPORTANT
    #
    # Mandatory first.
    # Optional after them.
    # --------------------------------------------------------

    all_bins = (
        mandatory_bins +
        optional_bins
    )

    # --------------------------------------------------------
    # Locations
    # --------------------------------------------------------

    locations = [depot]

    for bin_data in all_bins:

        locations.append(
            (
                bin_data["lat"],
                bin_data["lon"]
            )
        )

    # --------------------------------------------------------
    # Distance matrix
    # --------------------------------------------------------

    distance_matrix = build_distance_matrix(
        locations
    )

    # --------------------------------------------------------
    # OR-TOOLS MANAGER
    # --------------------------------------------------------

    manager = pywrapcp.RoutingIndexManager(
        len(locations),
        1,
        0
    )

    # --------------------------------------------------------
    # ROUTING MODEL
    # --------------------------------------------------------

    routing = pywrapcp.RoutingModel(
        manager
    )

    # --------------------------------------------------------
    # DISTANCE CALLBACK
    # --------------------------------------------------------

    def distance_callback(
        from_index,
        to_index
    ):

        from_node = manager.IndexToNode(
            from_index
        )

        to_node = manager.IndexToNode(
            to_index
        )

        return distance_matrix[
            from_node
        ][
            to_node
        ]

    transit_callback_index = (
        routing.RegisterTransitCallback(
            distance_callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    # --------------------------------------------------------
    # OPTIONAL BINS
    #
    # OR-Tools is allowed to skip them.
    # --------------------------------------------------------

    for i in range(
        len(mandatory_bins) + 1,
        len(all_bins) + 1
    ):

        index = manager.NodeToIndex(i)

        routing.AddDisjunction(
            [index],
            5000
        )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy
        .PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic
        .GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = 5

    # --------------------------------------------------------
    # SOLVE
    # --------------------------------------------------------

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:

        return None

    # --------------------------------------------------------
    # EXTRACT ROUTE
    # --------------------------------------------------------

    route = []

    index = routing.Start(0)

    while not routing.IsEnd(index):

        node_index = manager.IndexToNode(
            index
        )

        # DEPOT
        if node_index == 0:

            route.append({
                "type": "depot"
            })

        # BIN
        else:

            bin_data = all_bins[
                node_index - 1
            ]

            route.append({

                "type": "bin",

                "bin_id":
                    bin_data["bin_id"],

                "lat":
                    bin_data["lat"],

                "lon":
                    bin_data["lon"],

                "fill":
                    bin_data["fill"],

                "mandatory":
                    (
                        node_index
                        <= len(mandatory_bins)
                    )
            })

        index = solution.Value(
            routing.NextVar(index)
        )

    # Final depot

    route.append({
        "type": "depot"
    })

    return route