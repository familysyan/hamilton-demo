def test_create_and_list_todos(client):
    create_response = client.post("/api/todos", json={"title": "Buy milk"})
    assert create_response.status_code == 201
    created_todo = create_response.get_json()
    assert created_todo["id"] == 1
    assert created_todo["title"] == "Buy milk"
    assert created_todo["is_completed"] is False
    assert created_todo["completed_at"] is None

    list_response = client.get("/api/todos")
    assert list_response.status_code == 200
    todos = list_response.get_json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Buy milk"


def test_mark_todo_complete(client):
    create_response = client.post("/api/todos", json={"title": "Write tests"})
    todo_id = create_response.get_json()["id"]

    complete_response = client.patch(f"/api/todos/{todo_id}/complete")
    assert complete_response.status_code == 200
    completed_todo = complete_response.get_json()
    assert completed_todo["is_completed"] is True
    assert completed_todo["completed_at"] is not None


def test_create_todo_requires_title(client):
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 400
    assert response.get_json()["error"] == "title is required"
