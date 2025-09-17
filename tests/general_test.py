import pytest

from fastapi.testclient import TestClient
from homework.database import Base, engine
from homework.main import app


@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_requests(client):
    recipe_data = {
        "dish_name": "Пельмени",
        "cooking_time": 20,
        "ingredients": "мука, мясо",
        "description": "Сварить в кастрюле"
    }
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 200
    response = client.get("/recipes")
    assert response.status_code == 200
    response = client.get("/recipes/1")
    assert response.status_code == 200
