from flask import Blueprint, jsonify, request
from psycopg.rows import dict_row

from .db import get_connection

api = Blueprint("api", __name__)


@api.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@api.get("/api/ping")
def ping():
    return jsonify({"message": "pong"}), 200


def _serialize_todo(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "is_completed": row["is_completed"],
        "created_at": row["created_at"].isoformat(),
        "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
    }


@api.get("/api/todos")
def list_todos():
    completed_param = request.args.get("completed")
    completed_filter = None
    if completed_param is not None:
        lowered = completed_param.strip().lower()
        if lowered in {"true", "1"}:
            completed_filter = True
        elif lowered in {"false", "0"}:
            completed_filter = False
        else:
            return jsonify({"error": "completed must be true or false"}), 400

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            if completed_filter is None:
                cur.execute(
                    """
                    SELECT id, title, is_completed, created_at, completed_at
                    FROM todos
                    ORDER BY id ASC
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT id, title, is_completed, created_at, completed_at
                    FROM todos
                    WHERE is_completed = %s
                    ORDER BY id ASC
                    """,
                    (completed_filter,),
                )
            rows = cur.fetchall()
    return jsonify([_serialize_todo(row) for row in rows]), 200


@api.post("/api/todos")
def create_todo():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO todos (title)
                VALUES (%s)
                RETURNING id, title, is_completed, created_at, completed_at
                """,
                (title,),
            )
            row = cur.fetchone()

    return jsonify(_serialize_todo(row)), 201


@api.patch("/api/todos/<int:todo_id>/complete")
def mark_todo_complete(todo_id: int):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE todos
                SET is_completed = TRUE, completed_at = NOW()
                WHERE id = %s
                RETURNING id, title, is_completed, created_at, completed_at
                """,
                (todo_id,),
            )
            row = cur.fetchone()

    if row is None:
        return jsonify({"error": "todo not found"}), 404

    return jsonify(_serialize_todo(row)), 200


@api.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            deleted_count = cur.rowcount

    if deleted_count == 0:
        return jsonify({"error": "todo not found"}), 404

    return jsonify({"status": "deleted", "id": todo_id}), 200
