import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from uuid import uuid4

from src.infrastructure.data.postgres.base import Base
from src.presentation.api.routes.main import create_app

@pytest_asyncio.fixture(autouse=True)
async def clean_db(test_session_maker):
    async with test_session_maker() as session:
        await session.execute(text("SET session_replication_role = 'replica';"))
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))
        await session.execute(text("SET session_replication_role = 'origin';"))
        await session.commit()

@pytest_asyncio.fixture
async def async_client(test_session_maker):
    app = create_app(session_maker=test_session_maker)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_get_camera(async_client):
    camera_id = str(uuid4())
    payload = {
    "camera_id": camera_id,
    "camera_class_cd": 3,
    "camera_class": "Outdoor",
    "model": "modelX",
    "camera_name": "Entrance Gate Camera",
    "camera_place": "Main Entrance, Building A",
    "camera_place_cd": 12,
    "serial_number": "SN-A1B2C3D4",
    "camera_type_cd": 5,
    "camera_type": "PTZ",
    "camera_latitude": 52.371237,
    "camera_longitude": 4.895168,
    "archive": False,
    "azimuth": 180
    }

    resp = await async_client.post("/cameras/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    id = data["id"]
    assert data["camera_id"] == camera_id
    assert data["camera_class"] == "Outdoor"

    resp = await async_client.get(f"/cameras/{id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["camera_id"] == camera_id
    assert data["model"] == "modelX"

@pytest.mark.asyncio
async def test_update_camera(async_client):
    camera_id = str(uuid4())
    payload = {
    "camera_id": camera_id,
    "camera_class_cd": 3,
    "camera_class": "Outdoor",
    "model": "modelX",
    "camera_name": "Entrance Gate Camera",
    "camera_place": "Main Entrance, Building A",
    "camera_place_cd": 12,
    "serial_number": "SN-A1B2C3D4",
    "camera_type_cd": 5,
    "camera_type": "PTZ",
    "camera_latitude": 52.371237,
    "camera_longitude": 4.895168,
    "archive": False,
    "azimuth": 180
    }
    await async_client.post("/cameras", json=payload)

    resp = await async_client.post("/cameras/", json=payload)
    data = resp.json()
    id = data["id"]


    get_resp = await async_client.get(f"/cameras/{id}")
    full_data = get_resp.json()

    full_data["camera_name"] = "NewName"
    full_data["archive"] = True


    resp = await async_client.put(f"/cameras/{id}", json=full_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["camera_name"] == "NewName"
    assert data["archive"] is True


@pytest.mark.asyncio
async def test_geojson_endpoint(async_client):
    cam1 = {"camera_id": str(uuid4()), "camera_class_cd": 1, "camera_class": "A", "model": "X", "camera_name": "Cam1", "camera_place": "Loc1", "camera_place_cd": 1, "serial_number": "SN1", "camera_type_cd": 1, "camera_type": "T1", "camera_latitude": 1.1, "camera_longitude": 2.2, "archive": False, "azimuth": 10}
    cam2 = {"camera_id": str(uuid4()), "camera_class_cd": 2, "camera_class": "B", "model": "Y", "camera_name": "Cam2", "camera_place": "Loc2", "camera_place_cd": 2, "serial_number": "SN2", "camera_type_cd": 2, "camera_type": "T2", "camera_latitude": 3.3, "camera_longitude": 4.4, "archive": False, "azimuth": 20}
    await async_client.post("/cameras", json=cam1)
    await async_client.post("/cameras", json=cam2)

    resp = await async_client.get("/cameras/geojson")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "FeatureCollection"
    features = data["features"]
    for feat in features:
        props = feat["properties"]
        assert set(props.keys()) == {"camera_id", "has_video"}
    camera_ids = {feat["properties"]["camera_id"] for feat in features}
    assert camera_ids == {cam1["camera_id"], cam2["camera_id"]}

    assert all(not feat["properties"]["has_video"] for feat in features)
