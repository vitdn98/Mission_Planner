# Mission_Planner
This is a lightweight web-based dashboard built with Flask and PostgreSQL for planning and managing tactical missions. It includes full CRUD support for core entities like:

* Missions – Create, edit, and delete mission entries with status, description, and assigned location.

* Locations – Manage mission locations with name and geographic coordinates.

* Roles – Assign personnel to specific mission roles (e.g., Commander, Medic).

* Equipment – Track and assign equipment to missions with quantity control.

🛠️ Tech Stack
* Backend: Flask with Blueprints, using psycopg2 and connection pooling

* Frontend: HTML + Bootstrap for styling, vanilla JS for interactivity

* Database: PostgreSQL with tables for missions, locations, roles, equipment, and their associations

📁 Features
✅ Dashboard overview

✅ CRUD for missions and locations

✅ Assignments for roles and equipment

✅ Dynamic forms with JavaScript fetch API

✅ Styled using Bootstrap for responsive UI

✅ RESTful API endpoints for async actions
