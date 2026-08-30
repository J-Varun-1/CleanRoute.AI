from service.route_optimizer import optimize_route


bins = [
    {
        "bin_id": "BIN_001",
        "lat": 19.0760,
        "lon": 72.8777
    },
    {
        "bin_id": "BIN_002",
        "lat": 19.0800,
        "lon": 72.8800
    },
    {
        "bin_id": "BIN_003",
        "lat": 19.0700,
        "lon": 72.8700
    },
    {
        "bin_id": "BIN_004",
        "lat": 19.0850,
        "lon": 72.8650
    }
]


depot = (19.0750, 72.8770)


result = optimize_route(
    bins,
    depot
)


print("\n==============================")
print("OPTIMIZED ROUTE")
print("==============================")

for i, point in enumerate(result["route"]):

    if point["type"] == "depot":

        print(f"{i}. DEPOT")

    else:

        print(
            f"{i}. {point['bin_id']} "
            f"({point['lat']}, {point['lon']})"
        )


print("\nTotal Cost:", result["total_cost"])