from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from core.solomon_parser import parse_solomon_instance
from core.qaco_vrptw_engine import QACOVRPTW

app = FastAPI(title="QACO VRPTW Optimizer API")

class OptimizationRequest(BaseModel):
    dataset_name: str  # e.g., "c101"
    ants: int = 20
    iterations: int = 50

@app.post("/api/optimize-fleet")
def optimize_fleet(req: OptimizationRequest):
    # Construct path assuming data is at project root / data / solomon_instances
    file_path = f"../data/solomon_instances/{req.dataset_name}.csv"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Dataset {req.dataset_name} not found.")
        
    instance_data = parse_solomon_instance(file_path)
    
    optimizer = QACOVRPTW(
        instance_data=instance_data,
        num_ants=req.ants,
        iterations=req.iterations
    )
    
    routes, num_vehicles, total_distance = optimizer.run()
    
    return {
        "dataset": req.dataset_name,
        "total_vehicles_used": num_vehicles,
        "total_fleet_distance": round(total_distance, 2),
        "routes": routes
    }