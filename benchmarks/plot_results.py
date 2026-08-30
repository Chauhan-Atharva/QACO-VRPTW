import matplotlib.pyplot as plt

def plot_route_network(coords, routes, dataset_name, save_path="benchmarks/plots/routes.png"):
    """
    Plots vehicle fleet routes on a 2D coordinate grid.
    """
    plt.figure(figsize=(10, 8))
    
    # Plot Depot
    plt.scatter(coords[0][0], coords[0][1], c='red', s=200, marker='s', label='Depot')
    
    # Plot Customers
    plt.scatter(coords[1:, 0], coords[1:, 1], c='blue', s=50, alpha=0.6, label='Customers')
    
    # Plot Routes
    colors = plt.cm.get_cmap('tab20', len(routes))
    for idx, route in enumerate(routes):
        route_coords = [coords[node] for node in route]
        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]
        plt.plot(xs, ys, color=colors(idx), linewidth=1.5, label=f'Vehicle {idx+1}')

    plt.title(f"QACO Optimized Vehicle Routes - {dataset_name}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Route map saved to {save_path}")

def plot_convergence(qaco_history, dataset_name, save_path="benchmarks/plots/convergence.png"):
    """
    Plots algorithmic convergence over iterations.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(qaco_history, linewidth=2, color='purple', label='QACO Solution Cost')
    plt.title(f"Convergence Analysis - {dataset_name}")
    plt.xlabel("Iteration")
    plt.ylabel("Objective Cost (Z)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Convergence plot saved to {save_path}")