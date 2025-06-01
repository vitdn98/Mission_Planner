from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2

missions_bp = Blueprint("missions", __name__)


@missions_bp.route("/")
def list_missions():
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, status, location_id
                FROM missions
                ORDER BY created_at DESC
            """
            )
            missions = [
                {
                    "id": mission_id,
                    "name": name,
                    "status": status,
                    "location_id": location_id,
                }
                for mission_id, name, status, location_id in cur.fetchall()
            ]
        return render_template("missions.html", missions=missions)
    finally:
        current_app.db_pool.putconn(conn)


@missions_bp.route("/create", methods=["POST"])
def create_mission():
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO missions (name, description, status, location_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """,
                (
                    data["name"],
                    data["description"],
                    data["status"],
                    data["location_id"],
                ),
            )
            mission_id = cur.fetchone()[0]
            conn.commit()
        return jsonify({"id": mission_id, "message": "Mission created"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@missions_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_mission(id):
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM missions WHERE id=%s", (id,))
            conn.commit()
        return jsonify({"message": "Mission deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@missions_bp.route("/edit/<int:id>", methods=["PUT"])
def edit_mission(id):
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE missions
                SET name=%s, description=%s, status=%s, location_id=%s
                WHERE id=%s
            """,
                (
                    data["name"],
                    data.get("description", ""),
                    data["status"],
                    data["location_id"],
                    id,
                ),
            )
            conn.commit()
        return jsonify({"message": "Mission updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)
