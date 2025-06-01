from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2

roles_bp = Blueprint("roles", __name__)


@roles_bp.route("/")
def list_roles():
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM roles")
            rows = cur.fetchall()
            roles = [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]
        return render_template("roles.html", roles=roles)
    finally:
        current_app.db_pool.putconn(conn)


@roles_bp.route("/assign", methods=["POST"])
def assign_role():
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO mission_roles (mission_id, role_id, personnel)
                VALUES (%s, %s, %s)
            """,
                (data["mission_id"], data["role_id"], data["personnel"]),
            )
            conn.commit()
        return jsonify({"message": "Role assigned"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@roles_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_role(id):
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM roles WHERE id=%s", (id,))
            conn.commit()
        return jsonify({"message": "Role deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)


@roles_bp.route("/edit/<int:id>", methods=["PUT"])
def edit_role(id):
    data = request.json
    conn = current_app.db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE roles SET name=%s, description=%s WHERE id=%s
            """,
                (data["name"], data["description"], id),
            )
            conn.commit()
        return jsonify({"message": "Role updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_app.db_pool.putconn(conn)
