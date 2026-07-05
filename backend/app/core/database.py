"""
Fleet-[Client] Backend — Database Configuration
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=20,
    max_overflow=10,
)

# Create session factory
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# ========== Fleet Models ==========

class Vehicle(Base):
    """Fleet vehicle model."""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    vin = Column(String(17), unique=True)
    license_plate = Column(String(20))
    group_id = Column(String(50))
    status = Column(String(20), default="active")  # active, inactive, maintenance

    # Current state
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(200))
    speed = Column(Float)
    fuel_level = Column(Float)
    odometer = Column(Float)
    engine_hours = Column(Float)
    engine_status = Column(String(20))

    # Metadata
    samsara_id = Column(String(50))
    motive_id = Column(String(50))
    fleetio_id = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Driver(Base):
    """Fleet driver model."""
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    license_number = Column(String(50))
    license_state = Column(String(2))

    # HOS Status
    hos_driving_minutes = Column(Integer, default=0)
    hos_on_duty_minutes = Column(Integer, default=0)
    hos_remaining_minutes = Column(Integer)
    hos_cycle_hours = Column(Float)

    # Current assignment
    current_vehicle_id = Column(String(50))
    status = Column(String(20), default="available")  # driving, on_duty, off_duty, sleeper

    # Metadata
    samsara_id = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FaultCode(Base):
    """Vehicle fault code model."""
    __tablename__ = "fault_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(50), nullable=False, index=True)
    fault_code = Column(String(20), nullable=False)
    description = Column(String(200))
    severity = Column(String(20))  # critical, warning, info
    system = Column(String(50))  # engine, transmission, brake, etc.
    status = Column(String(20), default="active")  # active, resolved, acknowledged
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    occurrence_count = Column(Integer, default=1)
    resolved_at = Column(DateTime(timezone=True))


class FuelTransaction(Base):
    """Fuel transaction model."""
    __tablename__ = "fuel_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(50), nullable=False, index=True)
    driver_id = Column(String(50))
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    gallons = Column(Float)
    cost_per_gallon = Column(Float)
    total_cost = Column(Float)
    odometer = Column(Float)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    fuel_type = Column(String(20))
    anomaly_flag = Column(Boolean, default=False)
    anomaly_reason = Column(String(200))

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """Audit log for all agent actions."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    action_type = Column(String(50), nullable=False)  # alert, escalation, query, action
    severity = Column(String(20))  # critical, high, medium, low
    vehicle_id = Column(String(50))
    driver_id = Column(String(50))
    description = Column(Text, nullable=False)
    details = Column(JSON)
    agent_decision = Column(String(50))  # auto_act, escalated, logged
    human_response = Column(String(50))  # approved, rejected, timeout, null
    human_responder = Column(String(100))
    outcome = Column(String(100))
    cost = Column(Float)


class Escalation(Base):
    """Human escalation requests."""
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    escalation_id = Column(String(100), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    vehicle_id = Column(String(50))
    driver_id = Column(String(50))
    severity = Column(String(20), nullable=False)
    issue_type = Column(String(50))
    description = Column(Text, nullable=False)
    details = Column(JSON)
    recommended_action = Column(Text)
    cost_estimate = Column(Float)

    # Status tracking
    status = Column(String(20), default="pending")  # pending, approved, rejected, timeout
    channel = Column(String(20))  # telegram, email, sms
    sent_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))
    response_by = Column(String(100))
    response_notes = Column(Text)

    # Resolution
    resolution = Column(Text)
    resolution_cost = Column(Float)


# ========== Database Lifecycle ==========

async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")


async def get_session() -> AsyncSession:
    """Get a database session."""
    async with async_session() as session:
        yield session
