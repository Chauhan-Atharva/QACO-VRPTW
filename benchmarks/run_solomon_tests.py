import sys
import os
import time

# Dynamically find the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from backend.core.solomon_parser import parse_solomon_instance
from backend.core.qaco_vrptw_engine import QACOVRPTW

def run_benchmark(dataset_name):
    # Safely construct the path to the dataset
    file_path = os.path.join(project_root, "data", "solomon_instances", f"{dataset_name}.csv")
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find dataset at {file_path}")
        print("Ensure the file is named exactly as requested and placed in the correct folder.")
        return

    print(f"Loading {dataset_name}...")
    # Add max_capacity=200 for C1/R1/RC1 datasets, or 700 for C2 datasets
    instance_data = parse_solomon_instance(file_path, max_capacity=200)
    
    print(f"Running QACO VRPTW Engine (Nodes: {instance_data['num_nodes']})...")
    start_time = time.time()
    
    qaco = QACOVRPTW(instance_data, num_ants=50, iterations=300)
    routes, num_vehicles, distance = qaco.run()
    
    exec_time = time.time() - start_time
    
    print("\n--- OPTIMIZATION COMPLETE ---")
    print(f"Execution Time: {exec_time:.2f} seconds")
    print(f"Vehicles Used : {num_vehicles}")
    print(f"Total Distance: {distance:.2f}")
    print("Routes:")
    for i, route in enumerate(routes):
        print(f"  Vehicle {i+1}: {route}")

if __name__ == "__main__":
    # Ensure your filename matches this string exactly (e.g., "c101" vs "C101")
    run_benchmark("C101")