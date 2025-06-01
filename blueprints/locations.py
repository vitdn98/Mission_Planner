from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2

locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/")
def list_locations():
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, coordinates FROM locations")
            rows = cur.fetchall()
            locations = [{"id": r[0], "name": r[1], "coordinates": r[2]} for r in rows]
        return render_template("locations.html", locations=locations)
    finally:
        current_app.db_pool.putconn(conn)


@locations_bp.route("/create", methods=["POST"])
def create_location():
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO locations (name, coordinates) VALUES (%s, %s) RETURNING id",
                (data["name"], data["coordinates"]),
            )
            conn.commit()
            location_id = cur.fetchone()[0]
        return jsonify({"id": location_id, "message": "Location created"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@locations_bp.route("/update/<int:id>", methods=["PUT"])
def update_location(id):
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE locations SET name=%s, coordinates=%s WHERE id=%s",
                (data["name"], data["coordinates"], id),
            )
            conn.commit()
        return jsonify({"message": "Location updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@locations_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_location(id):
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM locations WHERE id=%s", (id,))
            conn.commit()
        return jsonify({"message": "Location deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)
