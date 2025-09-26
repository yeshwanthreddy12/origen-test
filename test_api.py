#!/usr/bin/env python3
"""
Simple script to test the API endpoints
Run this after starting the application with docker-compose up
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Origen.ai Simulation API...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test list machines
    print("\n2. Testing list machines...")
    response = requests.get(f"{BASE_URL}/machines/")
    print(f"   Status: {response.status_code}")
    machines = response.json()
    print(f"   Found {len(machines)} machines")
    
    if machines:
        machine_id = machines[0]["id"]
        print(f"   Using machine ID: {machine_id}")
        
        # Test create simulation
        print("\n3. Testing create simulation...")
        simulation_data = {
            "name": "test_simulation_api",
            "machine_id": machine_id
        }
        response = requests.post(f"{BASE_URL}/simulations/", json=simulation_data)
        print(f"   Status: {response.status_code}")
        simulation = response.json()
        print(f"   Created simulation: {simulation['name']} (ID: {simulation['id']})")
        
        simulation_id = simulation["id"]
        
        # Test get simulation details
        print("\n4. Testing get simulation details...")
        response = requests.get(f"{BASE_URL}/simulations/{simulation_id}/detailed")
        print(f"   Status: {response.status_code}")
        detailed = response.json()
        print(f"   Simulation with machine: {detailed['name']} on {detailed['machine']['name']}")
        
        # Test add convergence data
        print("\n5. Testing add convergence data...")
        for i in range(3):
            convergence_data = {
                "simulation_id": simulation_id,
                "loss_value": 1.0 - (i * 0.3)
            }
            response = requests.post(f"{BASE_URL}/convergence/data", json=convergence_data)
            print(f"   Added data point {i+1}: loss={convergence_data['loss_value']}")
            time.sleep(0.1)  # Small delay to see different timestamps
        
        # Test get convergence graph
        print("\n6. Testing get convergence graph...")
        response = requests.get(f"{BASE_URL}/convergence/{simulation_id}/graph")
        print(f"   Status: {response.status_code}")
        graph = response.json()
        print(f"   Graph data points: {len(graph['data_points'])}")
        print(f"   Is complete: {graph['is_complete']}")
        
        # Test list simulations
        print("\n7. Testing list simulations...")
        response = requests.get(f"{BASE_URL}/simulations/")
        print(f"   Status: {response.status_code}")
        simulations = response.json()
        print(f"   Total simulations: {simulations['total']}")
        
        # Test bare SQL operations
        print("\n8. Testing bare SQL operations...")
        
        # Create simulation with bare SQL
        response = requests.post(
            f"{BASE_URL}/simulations/{999}/create-bare-sql",
            params={"name": "bare_sql_test", "machine_id": machine_id}
        )
        print(f"   Bare SQL create simulation: {response.status_code}")
        
        # Add convergence data with bare SQL
        response = requests.post(
            f"{BASE_URL}/convergence/{simulation_id}/add-bare-sql",
            params={"loss_value": 0.1}
        )
        print(f"   Bare SQL add convergence data: {response.status_code}")
    
    print("\n✅ API testing completed!")
    print(f"\n📚 API Documentation available at: {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure to run 'docker-compose up' first.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
