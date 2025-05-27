import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from src.shared.database import Base
from src.main import create_app

@pytest_asyncio.fixture
async def clean_db(test_session_maker):
    async with test_session_maker() as session:
        await session.execute(text("SET session_replication_role = 'replica';"))
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))
        await session.execute(text("SET session_replication_role = 'origin';"))
        await session.commit()

@pytest_asyncio.fixture
def test_app(test_session_maker):
    return create_app(session_maker=test_session_maker)

@pytest.mark.asyncio
async def test_register_success(test_app, clean_db):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/register", json={
            "email": "testuser@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
    assert response.status_code == 201
    assert response.json()["detail"] == "User registered"

@pytest.mark.asyncio
async def test_register_duplicate(test_app, clean_db):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Первая регистрация
        await ac.post("/register", json={
            "email": "dupe@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
        # Повторная регистрация с тем же email
        response = await ac.post("/register", json={
            "email": "dupe@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(test_app, clean_db):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Сначала зарегистрируем пользователя
        await ac.post("/register", json={
            "email": "loginuser@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
        # Теперь логинимся
        response = await ac.post("/login", json={
            "email": "loginuser@example.com",
            "password": "password123"
        })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_wrong_password(test_app, clean_db):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Зарегистрируем пользователя
        await ac.post("/register", json={
            "email": "wrongpass@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
        # Пытаемся войти с неверным паролем
        response = await ac.post("/login", json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_refresh_success(test_app, clean_db):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Зарегистрируем и залогинимся
        await ac.post("/register", json={
            "email": "refreshuser@example.com",
            "password": "password123",
            "fio": "Test User",
            "org": "TestOrg"
        })
        login_resp = await ac.post("/login", json={
            "email": "refreshuser@example.com",
            "password": "password123"
        })
        refresh_token = login_resp.json()["refresh_token"]
        # Обновляем токен
        response = await ac.post("/refresh", json={
            "refresh_token": refresh_token
        })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data