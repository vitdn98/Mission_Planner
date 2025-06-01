from flask import Flask, render_template
from blueprints.missions import missions_bp
from blueprints.roles import roles_bp
from blueprints.equipment import equipment_bp
from blueprints.locations import locations_bp
import psycopg2
from psycopg2 import pool

app = Flask(__name__)

# Database connection pool
app.config["DB_CONFIG"] = {
    "dbname": "mission_planner",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432",
}
app.db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, **app.config["DB_CONFIG"])

# Register blueprints
app.register_blueprint(missions_bp, url_prefix="/missions")
app.register_blueprint(roles_bp, url_prefix="/roles")
app.register_blueprint(equipment_bp, url_prefix="/equipment")
app.register_blueprint(locations_bp, url_prefix="/locations")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
