from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


class Metrics(Base):
    __tablename__ = "metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String, nullable=False)
    time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lane_occupancy = relationship(
        "LaneOccupancy", back_populates="metric", cascade="all, delete"
    )
    vehicle_distribution = relationship(
        "VehicleDistribution", back_populates="metric", cascade="all, delete"
    )
    vehicle_counts = relationship(
        "VehicleCounts", back_populates="metric", cascade="all, delete"
    )


class LaneOccupancy(Base):
    __tablename__ = "lane_occupancy"

    lane_id = Column(Integer, primary_key=True, autoincrement=True)
    metrics_id = Column(Integer, ForeignKey("metrics.metric_id"), nullable=False)
    lane_name = Column(String, nullable=False)
    occupancy_rate = Column(Float, nullable=False)

    metric = relationship("Metrics", back_populates="lane_occupancy")


class VehicleDistribution(Base):
    __tablename__ = "vehicle_distribution"

    distribution_id = Column(Integer, primary_key=True, autoincrement=True)
    metrics_id = Column(Integer, ForeignKey("metrics.metric_id"), nullable=False)
    lane_name = Column(String, nullable=False)
    car = Column(Integer, default=0)
    truck = Column(Integer, default=0)
    motorcycle = Column(Integer, default=0)
    bus = Column(Integer, default=0)
    other = Column(Integer, default=0)

    metric = relationship("Metrics", back_populates="vehicle_distribution")


class VehicleCounts(Base):
    __tablename__ = "vehicle_counts"

    count_id = Column(Integer, primary_key=True, autoincrement=True)
    metrics_id = Column(Integer, ForeignKey("metrics.metric_id"), nullable=False)
    lane_name = Column(String, nullable=False)
    count_minute = Column(Float, nullable=False)
    count_hour = Column(Float, nullable=False)

    metric = relationship("Metrics", back_populates="vehicle_counts")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
