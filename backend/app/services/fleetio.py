"""
Fleetio Maintenance API Service
"""

import httpx
import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings

logger = structlog.get_logger()


class FleetioService:
    """Service for interacting with the Fleetio API."""

    def __init__(self):
        self.base_url = settings.FLEETIO_BASE_URL
        self.api_token = settings.FLEETIO_API_TOKEN
        self.account_token = settings.FLEETIO_ACCOUNT_TOKEN
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Account-Token": self.account_token,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Fleetio API."""
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

    async def get_vehicles(self) -> List[Dict]:
        """Get list of all vehicles."""
        data = await self._request("GET", "/vehicles")
        return data if isinstance(data, list) else data.get("records", [])

    async def get_work_orders(
        self,
        vehicle_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict]:
        """Get work orders."""
        params = {}
        if vehicle_id:
            params["vehicle_id"] = vehicle_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/work_orders", params=params)
        return data if isinstance(data, list) else data.get("records", [])

    async def get_service_entries(
        self,
        vehicle_id: Optional[str] = None,
        days: int = 30,
    ) -> List[Dict]:
        """Get service history entries."""
        params = {}
        if vehicle_id:
            params["vehicle_id"] = vehicle_id

        data = await self._request("GET", "/service_entries", params=params)
        entries = data if isinstance(data, list) else data.get("records", [])

        # Filter by date
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            e for e in entries
            if datetime.fromisoformat(e.get("date", "2000-01-01").replace("Z", "+00:00")) > cutoff
        ]

    async def get_fuel_entries(
        self,
        vehicle_id: Optional[str] = None,
        days: int = 30,
    ) -> List[Dict]:
        """Get fuel transaction entries."""
        params = {}
        if vehicle_id:
            params["vehicle_id"] = vehicle_id

        data = await self._request("GET", "/fuel_entries", params=params)
        entries = data if isinstance(data, list) else data.get("records", [])

        # Filter by date
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            e for e in entries
            if datetime.fromisoformat(e.get("date", "2000-01-01").replace("Z", "+00:00")) > cutoff
        ]

    async def get_maintenance_costs(
        self,
        vehicle_id: Optional[str] = None,
        days: int = 30,
    ) -> Dict:
        """Get maintenance cost summary."""
        entries = await self.get_service_entries(vehicle_id=vehicle_id, days=days)

        total_cost = sum(e.get("total_cost", 0) for e in entries)
        vehicle_count = len(set(e.get("vehicle_id") for e in entries))

        return {
            "entries": entries,
            "total_cost": total_cost,
            "entry_count": len(entries),
            "vehicle_count": vehicle_count,
            "average_per_vehicle": total_cost / vehicle_count if vehicle_count > 0 else 0,
            "period_days": days,
        }

    async def create_work_order(
        self,
        vehicle_id: str,
        service_type: str,
        notes: Optional[str] = None,
    ) -> Dict:
        """Create a new work order."""
        data = {
            "vehicle_id": vehicle_id,
            "service_type": service_type,
            "notes": notes,
        }
        return await self._request("POST", "/work_orders", json_data=data)
