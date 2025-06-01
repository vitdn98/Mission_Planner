from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2

equipment_bp = Blueprint("equipment", __name__)


@equipment_bp.route("/")
def list_equipment():
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, type FROM equipment")
            rows = cur.fetchall()
            equipment = [{"id": r[0], "name": r[1], "type": r[2]} for r in rows]
        return render_template("equipment.html", equipment=equipment)
    finally:
        current_app.db_pool.putconn(conn)


@equipment_bp.route("/assign", methods=["POST"])
def assign_equipment():
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO mission_equipment (mission_id, equipment_id, quantity)
                VALUES (%s, %s, %s)
            """,
                (data["mission_id"], data["equipment_id"], data["quantity"]),
            )
            conn.commit()
        return jsonify({"message": "Equipment assigned"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@equipment_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_equipment(id):
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM equipment WHERE id=%s", (id,))
            conn.commit()
        return jsonify({"message": "Equipment deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@equipment_bp.route("/edit/<int:id>", methods=["PUT"])
def edit_equipment(id):
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE equipment SET name=%s, type=%s WHERE id=%s
            """,
                (data["name"], data["type"], id),
            )
            conn.commit()
        return jsonify({"message": "Equipment updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)
