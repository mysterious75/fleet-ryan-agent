"""
Pydantic schemas for API request/response models.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== Vehicle Schemas ==========

class VehicleLocation(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    heading: Optional[float] = None


class VehicleResponse(BaseModel):
    vehicle_id: str
    name: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vin: Optional[str] = None
    status: str = "active"
    location: Optional[VehicleLocation] = None
    speed: Optional[float] = None
    fuel_level: Optional[float] = None
    odometer: Optional[float] = None
    engine_status: Optional[str] = None
    last_updated: Optional[datetime] = None


class VehicleListResponse(BaseModel):
    vehicles: List[VehicleResponse]
    total: int
    timestamp: datetime


class VehicleStatsResponse(BaseModel):
    vehicle_id: str
    location: Optional[VehicleLocation] = None
    speed: Optional[float] = None
    fuel_level: Optional[float] = None
    odometer: Optional[float] = None
    engine_hours: Optional[float] = None
    engine_status: Optional[str] = None
    battery_voltage: Optional[float] = None
    coolant_temperature: Optional[float] = None
    oil_pressure: Optional[float] = None
    last_updated: datetime


# ========== Fleet Overview ==========

class FleetOverviewResponse(BaseModel):
    total_vehicles: int
    active_vehicles: int
    idling_vehicles: int
    parked_vehicles: int
    offline_vehicles: int
    vehicles_with_faults: int
    overdue_maintenance: int
    total_miles_today: Optional[float] = None
    total_fuel_today: Optional[float] = None
    timestamp: datetime


# ========== Compliance Schemas ==========

class HOSDriverStatus(BaseModel):
    driver_id: str
    driver_name: str
    vehicle_id: Optional[str] = None
    status: str  # driving, on_duty, off_duty, sleeper
    driving_minutes_used: int
    driving_minutes_remaining: int
    on_duty_minutes_used: int
    on_duty_minutes_remaining: int
    cycle_hours_used: float
    cycle_hours_remaining: float
    near_limit: bool = False
    in_violation: bool = False
    next_break_required: Optional[datetime] = None


class HOSStatusResponse(BaseModel):
    drivers: List[HOSDriverStatus]
    total: int
    near_limit_count: int
    violations_count: int
    timestamp: datetime


class DVIRReport(BaseModel):
    dvir_id: str
    vehicle_id: str
    driver_id: str
    driver_name: str
    inspection_type: str  # pre_trip, post_trip
    status: str  # submitted, pending, overdue
    defects: List[Dict[str, Any]] = []
    submitted_at: Optional[datetime] = None
    due_at: Optional[datetime] = None


class DVIRStatusResponse(BaseModel):
    dvirs: List[DVIRReport]
    total: int
    submitted: int
    pending: int
    overdue: int
    timestamp: datetime


# ========== Maintenance Schemas ==========

class FaultCodeResponse(BaseModel):
    fault_code: str
    description: str
    severity: str  # critical, warning, info
    system: str  # engine, transmission, brake, etc.
    vehicle_id: str
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int
    status: str  # active, resolved


class MaintenanceScheduleItem(BaseModel):
    vehicle_id: str
    vehicle_name: str
    service_type: str
    due_miles: Optional[float] = None
    current_miles: Optional[float] = None
    due_date: Optional[datetime] = None
    overdue: bool = False
    due_soon: bool = False
    estimated_cost: Optional[float] = None


# ========== Escalation Schemas ==========

class EscalationCreate(BaseModel):
    vehicle_id: str
    severity: str = Field(..., description="critical, high, medium, low")
    issue_type: str
    description: str
    details: Optional[Dict[str, Any]] = None
    recommended_action: Optional[str] = None
    cost_estimate: Optional[float] = None


class EscalationResponse(BaseModel):
    escalation_id: str
    vehicle_id: str
    severity: str
    issue_type: str
    description: str
    status: str
    recommended_action: Optional[str] = None
    cost_estimate: Optional[float] = None
    created_at: datetime
    responded_at: Optional[datetime] = None
    response_by: Optional[str] = None


# ========== Webhook Schemas ==========

class WebhookEvent(BaseModel):
    platform: str  # samsara, motive, fleetio
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
