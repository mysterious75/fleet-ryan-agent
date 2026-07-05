"""
Mock Data Service — Realistic fleet data for demo/testing.
Use when real API keys are not available.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class MockDataService:
    """Generates realistic fleet data for demo purposes."""

    def __init__(self):
        self.vehicles = self._generate_vehicles()
        self.drivers = self._generate_drivers()
        self.fault_codes = self._generate_fault_codes()

    def _generate_vehicles(self) -> List[Dict]:
        """Generate 52 mock vehicles."""
        makes = ["Freightliner", "Peterbilt", "Kenworth", "Volvo", "Mack"]
        models = ["Cascadia", "579", "T680", "VNL", "Anthem"]
        cities = [
            ("Indianapolis, IN", 39.7684, -86.1581),
            ("Chicago, IL", 41.8781, -87.6298),
            ("Columbus, OH", 39.9612, -82.9988),
            ("Detroit, MI", 42.3314, -83.0458),
            ("Milwaukee, WI", 43.0389, -87.9065),
            ("Cincinnati, OH", 39.1031, -84.5120),
            ("St. Louis, MO", 38.6270, -90.1994),
            ("Nashville, TN", 36.1627, -86.7816),
            ("Louisville, KY", 38.2527, -85.7585),
            ("Minneapolis, MN", 44.9778, -93.2650),
        ]
        statuses = ["active", "active", "active", "active", "idle", "maintenance", "offline"]

        vehicles = []
        for i in range(1, 53):
            city = random.choice(cities)
            status = random.choice(statuses)
            make = random.choice(makes)
            model = random.choice(models)
            year = random.randint(2018, 2025)

            vehicles.append({
                "vehicle_id": f"TRUCK-{i:03d}",
                "name": f"Truck #{i}",
                "make": make,
                "model": model,
                "year": year,
                "vin": f"1HGCM82633A{random.randint(100000, 999999)}",
                "status": status,
                "location": {
                    "latitude": city[1] + random.uniform(-0.5, 0.5),
                    "longitude": city[2] + random.uniform(-0.5, 0.5),
                    "address": city[0],
                    "heading": random.randint(0, 359),
                },
                "speed": random.uniform(0, 75) if status == "active" else 0,
                "fuel_level": random.uniform(15, 95),
                "odometer": random.randint(50000, 250000),
                "engine_hours": random.randint(5000, 25000),
                "engine_status": "running" if status == "active" else "off",
                "last_updated": datetime.utcnow().isoformat(),
            })

        return vehicles

    def _generate_drivers(self) -> List[Dict]:
        """Generate 20 mock drivers."""
        names = [
            "Mike Johnson", "David Williams", "James Brown", "Robert Davis",
            "William Wilson", "Michael Martinez", "Richard Anderson", "Thomas Taylor",
            "Charles Thomas", "Daniel Jackson", "Matthew White", "Anthony Harris",
            "Mark Martin", "Donald Garcia", "Steven Robinson", "Paul Clark",
            "Andrew Lewis", "Joshua Lee", "Kenneth Walker", "Kevin Hall",
        ]
        statuses = ["driving", "driving", "on_duty", "off_duty", "sleeper"]

        drivers = []
        for i, name in enumerate(names, 1):
            driving_min = random.randint(0, 660)  # 0-11 hours
            remaining = max(0, 660 - driving_min)

            drivers.append({
                "driver_id": f"DRV-{i:03d}",
                "name": name,
                "email": f"{name.lower().replace(' ', '.')}@example.com",
                "phone": f"(317) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "current_vehicle_id": f"TRUCK-{random.randint(1, 52):03d}",
                "status": random.choice(statuses),
                "hos_driving_minutes": driving_min,
                "hos_remaining_minutes": remaining,
                "near_limit": remaining < 60,
                "in_violation": remaining < 0,
            })

        return drivers

    def _generate_fault_codes(self) -> List[Dict]:
        """Generate mock fault codes."""
        fault_definitions = [
            ("P0340", "Camshaft Position Sensor Circuit Malfunction", "critical", "engine"),
            ("P0300", "Random/Multiple Cylinder Misfire Detected", "warning", "engine"),
            ("P0401", "Exhaust Gas Recirculation Flow Insufficient", "warning", "engine"),
            ("P0420", "Catalyst System Efficiency Below Threshold", "info", "engine"),
            ("P0500", "Vehicle Speed Sensor Malfunction", "warning", "transmission"),
            ("P0700", "Transmission Control System Malfunction", "critical", "transmission"),
            ("C0035", "Left Front Wheel Speed Sensor", "warning", "brake"),
            ("C0040", "Right Front Wheel Speed Sensor", "warning", "brake"),
            ("B0001", "Airbag Warning Light", "critical", "body"),
            ("U0100", "Lost Communication with ECM", "critical", "network"),
        ]

        faults = []
        for i in range(15):
            fault = random.choice(fault_definitions)
            vehicle = random.choice(self.vehicles)

            faults.append({
                "fault_code": fault[0],
                "description": fault[1],
                "severity": fault[2],
                "system": fault[3],
                "vehicle_id": vehicle["vehicle_id"],
                "vehicle_name": vehicle["name"],
                "status": "active",
                "first_seen": (datetime.utcnow() - timedelta(days=random.randint(0, 7))).isoformat(),
                "last_seen": datetime.utcnow().isoformat(),
                "occurrence_count": random.randint(1, 10),
            })

        return faults

    def get_vehicles(self, group_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get mock vehicles with optional filters."""
        vehicles = self.vehicles.copy()

        if status:
            vehicles = [v for v in vehicles if v["status"] == status]

        return vehicles

    def get_vehicle(self, vehicle_id: str) -> Optional[Dict]:
        """Get a specific mock vehicle."""
        for v in self.vehicles:
            if v["vehicle_id"] == vehicle_id:
                return v
        return None

    def get_vehicle_stats(self, vehicle_id: str) -> Optional[Dict]:
        """Get mock vehicle stats."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return None

        return {
            "vehicle_id": vehicle_id,
            "location": vehicle["location"],
            "speed": vehicle["speed"],
            "fuel_level": vehicle["fuel_level"],
            "odometer": vehicle["odometer"],
            "engine_hours": vehicle["engine_hours"],
            "engine_status": vehicle["engine_status"],
            "battery_voltage": round(random.uniform(12.0, 14.5), 1),
            "coolant_temperature": random.randint(180, 220),
            "oil_pressure": random.randint(25, 65),
            "last_updated": datetime.utcnow().isoformat(),
        }

    def get_fleet_overview(self) -> Dict:
        """Get mock fleet overview."""
        active = sum(1 for v in self.vehicles if v["status"] == "active")
        idle = sum(1 for v in self.vehicles if v["status"] == "idle")
        maintenance = sum(1 for v in self.vehicles if v["status"] == "maintenance")
        offline = sum(1 for v in self.vehicles if v["status"] == "offline")

        return {
            "total_vehicles": len(self.vehicles),
            "active_vehicles": active,
            "idling_vehicles": idle,
            "parked_vehicles": len(self.vehicles) - active - idle - maintenance - offline,
            "offline_vehicles": offline,
            "vehicles_with_faults": len(set(f["vehicle_id"] for f in self.fault_codes)),
            "overdue_maintenance": random.randint(0, 5),
            "total_miles_today": random.randint(10000, 20000),
            "total_fuel_today": random.randint(1500, 3000),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_hos_status(self, driver_id: Optional[str] = None, near_limit: bool = False) -> List[Dict]:
        """Get mock HOS status."""
        drivers = self.drivers.copy()

        if driver_id:
            drivers = [d for d in drivers if d["driver_id"] == driver_id]

        if near_limit:
            drivers = [d for d in drivers if d["near_limit"]]

        return drivers

    def get_fault_codes(self, vehicle_id: Optional[str] = None, severity: Optional[str] = None) -> List[Dict]:
        """Get mock fault codes."""
        faults = self.fault_codes.copy()

        if vehicle_id:
            faults = [f for f in faults if f["vehicle_id"] == vehicle_id]

        if severity:
            faults = [f for f in faults if f["severity"] == severity]

        return faults

    def search_vehicles(self, query: str) -> List[Dict]:
        """Search mock vehicles."""
        query_lower = query.lower()
        return [
            v for v in self.vehicles
            if query_lower in v["name"].lower()
            or query_lower in v["vehicle_id"].lower()
            or query_lower in v["location"]["address"].lower()
            or query_lower in v["make"].lower()
            or query_lower in v["model"].lower()
        ]

    def get_compliance_summary(self) -> Dict:
        """Get mock compliance summary."""
        total_drivers = len(self.drivers)
        near_limit = sum(1 for d in self.drivers if d["near_limit"])
        violations = sum(1 for d in self.drivers if d["in_violation"])

        return {
            "total_drivers": total_drivers,
            "drivers_near_limit": near_limit,
            "drivers_in_violation": violations,
            "dvir_compliance": random.randint(85, 100),
            "ifta_status": "current",
        }

    def get_maintenance_schedule(self, days_ahead: int = 7) -> List[Dict]:
        """Get mock maintenance schedule."""
        schedule = []
        for i in range(8):
            vehicle = random.choice(self.vehicles)
            schedule.append({
                "vehicle_id": vehicle["vehicle_id"],
                "vehicle_name": vehicle["name"],
                "service_type": random.choice(["Oil Change", "Tire Rotation", "Brake Inspection", "DPF Cleaning"]),
                "due_miles": vehicle["odometer"] + random.randint(-500, 2000),
                "current_miles": vehicle["odometer"],
                "due_date": (datetime.utcnow() + timedelta(days=random.randint(0, days_ahead))).isoformat(),
                "overdue": random.random() < 0.2,
                "due_soon": random.random() < 0.3,
                "estimated_cost": random.randint(100, 800),
            })

        return schedule


# Global instance
mock_data = MockDataService()
