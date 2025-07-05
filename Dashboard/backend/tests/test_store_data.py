import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..src.db.db_model import Base
from ..src.db.store_metrics import store_metrics_data
from ..src.db.db_model import Metrics, LaneOccupancy, VehicleDistribution
from ..src.db.store_metrics import retrieve_metrics_data


@pytest.fixture(scope="function")
def db_session():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE env variable is not set")
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = engine.connect()
    transaction = connection.begin()
    session.bind = connection
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_store_metrics_data_writes_correctly(db_session):
    video_name = "testvideo"
    type_distribution = {"1": {"car": 3, "bus": 1}, "2": {"truck": 2}}
    occupancy = {"1": 0.5, "2": 0.8}

    store_metrics_data(db_session, video_name, type_distribution, occupancy)

    metric = db_session.query(Metrics).order_by(Metrics.metric_id.desc()).first()
    assert metric is not None
    assert metric.video_name.startswith(video_name + "_")
    metric_id = metric.metric_id

    occs = db_session.query(LaneOccupancy).filter_by(metrics_id=metric_id).all()
    assert len(occs) == 2
    occ_dict = {o.lane_name: o.occupancy_rate for o in occs}
    assert occ_dict["1"] == 0.5
    assert occ_dict["2"] == 0.8

    dists = db_session.query(VehicleDistribution).filter_by(metrics_id=metric_id).all()
    assert len(dists) == 2
    dist1 = next(d for d in dists if d.lane_name == "1")
    assert dist1.car == 3
    assert dist1.bus == 1
    assert dist1.truck == 0
    dist2 = next(d for d in dists if d.lane_name == "2")
    assert dist2.truck == 2


def test_retrieve_metrics_data_returns_expected_format(db_session):
    store_metrics_data(
        db_session,
        video_name="retrieve_test",
        type_distribution={"3": {"motorcycle": 4}},
        occupancy={"3": 0.7},
    )

    results = retrieve_metrics_data(db_session)
    assert isinstance(results, list)
    assert len(results) > 0
    latest = results[-1]

    assert "metric_id" in latest
    assert latest["video_name"].startswith("retrieve_test_")
    assert isinstance(latest["lane_occupancy"], list)
    assert isinstance(latest["vehicle_distribution"], list)

    occ = latest["lane_occupancy"][0]
    assert occ["lane_name"] == "3"
    assert occ["occupancy_rate"] == 0.7

    dist = latest["vehicle_distribution"][0]
    assert dist["lane_name"] == "3"
    assert dist["motorcycle"] == 4
