from fastapi.testclient import TestClient
from homework.main import app


client = TestClient(app)


def test_requests():
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
