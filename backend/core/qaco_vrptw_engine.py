import numpy as np
import random
import math

class QACOVRPTW:
    def __init__(self, instance_data, num_ants=20, iterations=100, theta_step=0.01*math.pi):
        self.d_matrix = instance_data["dist_matrix"]
        self.demands = instance_data["demands"]
        self.ready_times = instance_data["ready_times"]
        self.due_times = instance_data["due_times"]
        self.service_times = instance_data["service_times"]
        self.max_capacity = instance_data["max_capacity"]
        self.N = instance_data["num_nodes"]
        
        self.num_ants = num_ants
        self.iterations = iterations
        self.theta_step = theta_step
        
        # W1 for vehicles (heavy penalty), W2 for distance
        self.w_vehicles = 1000  
        self.w_distance = 1
        
        # Initialize (N)x(N) Quantum Matrix: [alpha, beta]
        init_val = 1.0 / math.sqrt(2)
        self.alpha_matrix = np.full((self.N, self.N), init_val)
        self.beta_matrix = np.full((self.N, self.N), init_val)
        np.fill_diagonal(self.alpha_matrix, 0)
        np.fill_diagonal(self.beta_matrix, 0)
        
        self.global_best_routes = []
        self.global_best_cost = float('inf')
        
    def dispatch_fleet(self):
        unvisited = set(range(1, self.N))
        fleet_routes = []
        
        while unvisited:
            route = [0] # Start at depot
            current_time = 0.0
            current_load = 0.0
            current_node = 0
            
            while True:
                valid_customers = []
                probabilities = []
                
                # Check constraints for all unvisited nodes
                for j in unvisited:
                    travel_time = self.d_matrix[current_node][j]
                    arrival_time = current_time + travel_time
                    
                    # Constraint check: Time window and Capacity
                    if arrival_time <= self.due_times[j] and (current_load + self.demands[j]) <= self.max_capacity:
                        valid_customers.append(j)
                        
                        # Calculate Heuristic (Eta)
                        urgency = max(1.0, self.due_times[j] - arrival_time)
                        dist = max(0.1, travel_time)
                        eta = 1.0 / (dist * urgency)
                        
                        # Quantum Probability = Beta^2 * Eta
                        quantum_prob = (self.beta_matrix[current_node][j] ** 2) * eta
                        probabilities.append(quantum_prob)
                
                if not valid_customers:
                    route.append(0) # Return to depot
                    break
                    
                # Roulette wheel selection
                total_prob = sum(probabilities)
                if total_prob == 0:
                    next_node = random.choice(valid_customers)
                else:
                    norm_probs = [p / total_prob for p in probabilities]
                    next_node = random.choices(valid_customers, weights=norm_probs, k=1)[0]
                
                # Update truck state
                route.append(next_node)
                unvisited.remove(next_node)
                
                arrival_time = current_time + self.d_matrix[current_node][next_node]
                # Wait if arriving before ready_time
                current_time = max(arrival_time, self.ready_times[next_node]) + self.service_times[next_node]
                current_load += self.demands[next_node]
                current_node = next_node
                
            fleet_routes.append(route)
            
        return fleet_routes

    def evaluate_cost(self, routes):
        total_vehicles = len(routes)
        total_distance = 0.0
        for route in routes:
            for i in range(len(route) - 1):
                total_distance += self.d_matrix[route[i]][route[i+1]]
        return (total_vehicles * self.w_vehicles) + (total_distance * self.w_distance), total_distance
        
    def apply_rotation_gate(self, best_routes):
        # Flatten routes to get all used edges
        used_edges = set()
        for route in best_routes:
            for i in range(len(route) - 1):
                used_edges.add((route[i], route[i+1]))
                
        for i in range(self.N):
            for j in range(self.N):
                if i == j: continue
                
                alpha_old = self.alpha_matrix[i][j]
                beta_old = self.beta_matrix[i][j]
                
                direction = 1 if (i, j) in used_edges else -1
                delta_theta = direction * self.theta_step
                
                alpha_new = (alpha_old * math.cos(delta_theta)) - (beta_old * math.sin(delta_theta))
                beta_new = (alpha_old * math.sin(delta_theta)) + (beta_old * math.cos(delta_theta))
                
                # Normalize
                norm = math.sqrt(alpha_new**2 + beta_new**2)
                if norm > 0:
                    self.alpha_matrix[i][j] = alpha_new / norm
                    self.beta_matrix[i][j] = beta_new / norm

    def run(self):
        for iteration in range(self.iterations):
            iteration_best_routes = []
            iteration_best_cost = float('inf')
            
            for _ in range(self.num_ants):
                routes = self.dispatch_fleet()
                cost, _ = self.evaluate_cost(routes)
                
                if cost < iteration_best_cost:
                    iteration_best_cost = cost
                    iteration_best_routes = routes
                    
                if cost < self.global_best_cost:
                    self.global_best_cost = cost
                    self.global_best_routes = routes
            
            if iteration_best_routes:
                self.apply_rotation_gate(iteration_best_routes)
                
        _, final_dist = self.evaluate_cost(self.global_best_routes)
        return self.global_best_routes, len(self.global_best_routes), final_dist