import requests
from ortools.constraint_solver import (
    routing_enums_pb2,
    pywrapcp
)


OSRM_URL = (
    "https://router.project-osrm.org"
)


def get_distance_matrix(locations):

    coordinates = ";".join(
        f"{lon},{lat}"
        for lat, lon in locations
    )

    url = (
        f"{OSRM_URL}/table/v1/driving/"
        f"{coordinates}"
        "?annotations=distance,duration"
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return (
        data["distances"],
        data["durations"]
    )


def optimize_route(
    distance_matrix,
    num_vehicles=1,
    depot=0
):

    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        num_vehicles,
        depot
    )

    routing = pywrapcp.RoutingModel(
        manager
    )

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

        return int(
            distance_matrix[
                from_node
            ][to_node]
        )

    transit_callback_index = (
        routing.RegisterTransitCallback(
            distance_callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

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

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if not solution:

        return None

    route = []

    index = routing.Start(0)

    while not routing.IsEnd(index):

        node = manager.IndexToNode(
            index
        )

        route.append(node)

        index = solution.Value(
            routing.NextVar(index)
        )

    route.append(
        manager.IndexToNode(index)
    )

    return route