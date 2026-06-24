from geopy.distance import geodesic


def calculate_distance(bin1, bin2):
    return geodesic(
        (bin1.latitude, bin1.longitude),
        (bin2.latitude, bin2.longitude)
    ).km


def nearest_neighbor_route(bins):

    if not bins:
        return [], 0

    unvisited = bins.copy()

    route = [unvisited.pop(0)]

    total_distance = 0

    while unvisited:

        current = route[-1]

        nearest = min(
            unvisited,
            key=lambda b: calculate_distance(
                current,
                b
            )
        )

        distance = calculate_distance(
            current,
            nearest
        )

        total_distance += distance

        route.append(nearest)

        unvisited.remove(nearest)

    return route, round(total_distance, 2)