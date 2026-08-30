import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

def parse_solomon_instance(file_path, max_capacity=200):
    """
    Parses a Solomon VRPTW Kaggle CSV file using pandas.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Strip any whitespace from column names just in case
    df.columns = df.columns.str.strip()
    
    # Identify columns by their general position or common Kaggle naming conventions
    # Assuming standard order: Cust No, X, Y, Demand, Ready, Due, Service
    coords = df.iloc[:, 1:3].values
    demands = df.iloc[:, 3].tolist()
    ready_times = df.iloc[:, 4].tolist()
    due_times = df.iloc[:, 5].tolist()
    service_times = df.iloc[:, 6].tolist()
    
    # Calculate N x N Euclidean distance matrix
    dist_matrix = distance_matrix(coords, coords)
    
    return {
        "max_capacity": max_capacity,
        "dist_matrix": dist_matrix,
        "demands": demands,
        "ready_times": ready_times,
        "due_times": due_times,
        "service_times": service_times,
        "num_nodes": len(coords)
    }