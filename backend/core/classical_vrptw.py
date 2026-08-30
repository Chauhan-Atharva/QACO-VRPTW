import numpy as np

def run_clarke_wright_vrptw(instance_data):
    """
    Classical Clarke-Wright Savings Heuristic adapted for VRPTW baseline comparison.
    """
    d_matrix = instance_data["dist_matrix"]
    demands = instance_data["demands"]
    ready_times = instance_data["ready_times"]
    due_times = instance_data["due_times"]
    service_times = instance_data["service_times"]
    max_cap = instance_data["max_capacity"]
    N = instance_data["num_nodes"]

    # Compute savings: S_ij = d_0i + d_0j - d_ij
    savings = []
    for i in range(1, N):
        for j in range(i + 1, N):
            s = d_matrix[0][i] + d_matrix[0][j] - d_matrix[i][j]
            savings.append((s, i, j))

    # Sort savings in descending order
    savings.sort(key=lambda x: x[0], reverse=True)

    # Initialize each customer in their own route: [0, i, 0]
    routes = [[0, i, 0] for i in range(1, N)]

    def get_route_and_position(node):
        for r_idx, route in enumerate(routes):
            if node in route:
                return r_idx, route.index(node)
        return None, None

    def is_valid_route(route):
        # Check capacity
        load = sum(demands[node] for node in route if node != 0)
        if load > max_cap:
            return False

        # Check time windows
        curr_time = 0.0
        for k in range(len(route) - 1):
            curr_node = route[k]
            next_node = route[k+1]
            travel_t = d_matrix[curr_node][next_node]
            arr_t = curr_time + travel_t

            if arr_t > due_times[next_node]:
                return False
            curr_time = max(arr_t, ready_times[next_node]) + service_times[next_node]

        return True

    # Merge routes based on savings list
    for s, i, j in savings:
        r_i_idx, pos_i = get_route_and_position(i)
        r_j_idx, pos_j = get_route_and_position(j)

        if r_i_idx != r_j_idx and r_i_idx is not None and r_j_idx is not None:
            route_i = routes[r_i_idx]
            route_j = routes[r_j_idx]

            # Try merging end of route_i with start of route_j
            if pos_i == len(route_i) - 2 and pos_j == 1:
                new_route = route_i[:-1] + route_j[1:]
                if is_valid_route(new_route):
                    routes[r_i_idx] = new_route
                    routes.pop(r_j_idx)

    # Calculate total fleet distance
    total_distance = 0.0
    for r in routes:
        for k in range(len(r) - 1):
            total_distance += d_matrix[r[k]][r[k+1]]

    return routes, len(routes), total_distance