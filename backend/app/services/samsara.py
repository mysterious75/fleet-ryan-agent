"""
Samsara Fleet API Service
"""

import httpx
import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings

logger = structlog.get_logger()


class SamsaraService:
    """Service for interacting with the Samsara Fleet API."""

    def __init__(self):
        self.base_url = settings.SAMSARA_BASE_URL
        self.api_token = settings.SAMSARA_API_TOKEN
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
        # Use mock data when API token is not set
        self.use_mock = not self.api_token
        if self.use_mock:
            from app.services.mock_data import mock_data
            self.mock = mock_data
            logger.info("Samsara API token not set — using mock data")

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Samsara API."""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_vehicles(
        self,
        group_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict]:
        """Get list of all vehicles."""
        if self.use_mock:
            return self.mock.get_vehicles(group_id=group_id, status=status)

        params = {}
        if group_id:
            params["groupId"] = group_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/v1/fleet/vehicles", params=params)
        return data.get("vehicles", [])

    async def get_vehicle(self, vehicle_id: str) -> Optional[Dict]:
        """Get details for a specific vehicle."""
        if self.use_mock:
            return self.mock.get_vehicle(vehicle_id)

        try:
            data = await self._request("GET", f"/v1/fleet/vehicles/{vehicle_id}")
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def get_vehicle_stats(self, vehicle_id: str) -> Optional[Dict]:
        """Get real-time vehicle stats."""
        if self.use_mock:
            return self.mock.get_vehicle_stats(vehicle_id)

        try:
            data = await self._request(
                "GET",
                "/v1/fleet/vehicles/stats",
                params={"id": vehicle_id},
            )
            vehicles = data.get("vehicles", [])
            return vehicles[0] if vehicles else None
        except Exception:
            return None

    async def get_fleet_overview(self) -> Dict:
        """Get fleet-wide overview statistics."""
        if self.use_mock:
            return self.mock.get_fleet_overview()

        vehicles = await self.get_vehicles()

        total = len(vehicles)
        active = sum(1 for v in vehicles if v.get("status") == "active")
        idling = sum(
            1
            for v in vehicles
            if v.get("engineStatus") == "on" and v.get("speed", 0) == 0
        )
        parked = sum(
            1
            for v in vehicles
            if v.get("engineStatus") == "off"
        )
        offline = sum(1 for v in vehicles if v.get("status") == "offline")

        return {
            "total_vehicles": total,
            "active_vehicles": active,
            "idling_vehicles": idling,
            "parked_vehicles": parked,
            "offline_vehicles": offline,
            "vehicles_with_faults": 0,  # TODO: integrate fault data
            "overdue_maintenance": 0,  # TODO: integrate maintenance data
            "timestamp": datetime.utcnow(),
        }

    async def get_vehicle_faults(self, vehicle_id: str) -> List[Dict]:
        """Get fault codes for a vehicle."""
        if self.use_mock:
            return self.mock.get_fault_codes(vehicle_id=vehicle_id)

        try:
            data = await self._request("GET", f"/v1/faults", params={"vehicleId": vehicle_id})
            return data.get("faults", [])
        except Exception:
            return []

    async def get_fleet_faults(
        self,
        vehicle_id: Optional[str] = None,
        severity: Optional[str] = None,
        status: str = "active",
    ) -> List[Dict]:
        """Get fleet-wide fault codes."""
        if self.use_mock:
            return self.mock.get_fault_codes(vehicle_id=vehicle_id, severity=severity)

        params = {"status": status}
        if vehicle_id:
            params["vehicleId"] = vehicle_id
        if severity:
            params["severity"] = severity

        try:
            data = await self._request("GET", "/v1/faults", params=params)
            return data.get("faults", [])
        except Exception:
            return []

    async def get_fault_patterns(self, days: int = 30) -> List[Dict]:
        """Analyze fault code patterns over time."""
        # TODO: Implement pattern analysis
        return []

    async def get_hos_status(
        self,
        driver_id: Optional[str] = None,
        near_limit: bool = False,
    ) -> List[Dict]:
        """Get HOS status for drivers."""
        if self.use_mock:
            return self.mock.get_hos_status(driver_id=driver_id, near_limit=near_limit)

        params = {}
        if driver_id:
            params["driverId"] = driver_id

        try:
            data = await self._request("GET", "/v1/fleet/drivers", params=params)
            drivers = data.get("drivers", [])

            result = []
            for driver in drivers:
                hos = driver.get("hos", {})
                driving_remaining = hos.get("drivingMsRemaining", 0) / 60000  # ms to min

                status = {
                    "driver_id": driver.get("id"),
                    "driver_name": driver.get("name"),
                    "vehicle_id": driver.get("vehicleId"),
                    "status": hos.get("status", "unknown"),
                    "driving_minutes_used": hos.get("drivingMs", 0) / 60000,
                    "driving_minutes_remaining": driving_remaining,
                    "near_limit": driving_remaining < 60,
                    "in_violation": driving_remaining < 0,
                }

                if near_limit and not status["near_limit"]:
                    continue
                result.append(status)

            return result
        except Exception:
            return []

    async def get_hos_violations(self) -> List[Dict]:
        """Get all current HOS violations."""
        drivers = await self.get_hos_status(near_limit=False)
        return [d for d in drivers if d.get("in_violation")]

    async def get_dvir_status(self, status: Optional[str] = None) -> List[Dict]:
        """Get DVIR status."""
        # TODO: Implement DVIR status from Samsara API
        return []

    async def get_ifta_status(self, quarter: Optional[str] = None) -> Dict:
        """Get IFTA status."""
        # TODO: Implement IFTA status from Samsara API
        return {"status": "not_implemented"}

    async def get_compliance_summary(self) -> Dict:
        """Get overall compliance summary."""
        if self.use_mock:
            return self.mock.get_compliance_summary()

        hos = await self.get_hos_status()
        return {
            "total_drivers": len(hos),
            "drivers_near_limit": sum(1 for d in hos if d.get("near_limit")),
            "drivers_in_violation": sum(1 for d in hos if d.get("in_violation")),
            "dvir_compliance": 0,  # TODO
            "ifta_status": "not_implemented",  # TODO
        }

    async def get_maintenance_schedule(
        self,
        vehicle_id: Optional[str] = None,
        days_ahead: int = 7,
    ) -> List[Dict]:
        """Get upcoming maintenance schedule."""
        if self.use_mock:
            return self.mock.get_maintenance_schedule(days_ahead=days_ahead)

        # TODO: Implement maintenance schedule from Samsara API
        return []

    async def search_vehicles(self, query: str) -> List[Dict]:
        """Search vehicles by name, ID, or location."""
        if self.use_mock:
            return self.mock.search_vehicles(query)

        vehicles = await self.get_vehicles()
        query_lower = query.lower()
        return [
            v
            for v in vehicles
            if query_lower in v.get("name", "").lower()
            or query_lower in v.get("id", "").lower()
            or query_lower in v.get("location", {}).get("address", "").lower()
        ]
