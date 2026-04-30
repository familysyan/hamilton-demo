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


def test_filter_todos_by_completion(client):
    first = client.post("/api/todos", json={"title": "Do laundry"}).get_json()
    second = client.post("/api/todos", json={"title": "Send email"}).get_json()

    client.patch(f"/api/todos/{second['id']}/complete")

    completed_response = client.get("/api/todos?completed=true")
    assert completed_response.status_code == 200
    completed = completed_response.get_json()
    assert len(completed) == 1
    assert completed[0]["id"] == second["id"]

    open_response = client.get("/api/todos?completed=false")
    assert open_response.status_code == 200
    open_todos = open_response.get_json()
    assert len(open_todos) == 1
    assert open_todos[0]["id"] == first["id"]


def test_delete_todo(client):
    created = client.post("/api/todos", json={"title": "Temporary task"}).get_json()

    delete_response = client.delete(f"/api/todos/{created['id']}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["status"] == "deleted"

    list_response = client.get("/api/todos")
    assert list_response.status_code == 200
    assert list_response.get_json() == []


def test_delete_todo_not_found(client):
    response = client.delete("/api/todos/9999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "todo not found"
