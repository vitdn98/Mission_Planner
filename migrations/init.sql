\c mission_planner;

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    coordinates VARCHAR(50) NOT NULL
);

CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    location_id INTEGER REFERENCES locations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'available'
);

CREATE TABLE mission_roles (
    id SERIAL PRIMARY KEY,
    mission_id INTEGER REFERENCES missions(id),
    role_id INTEGER REFERENCES roles(id),
    personnel VARCHAR(100) NOT NULL
);

CREATE TABLE mission_equipment (
    id SERIAL PRIMARY KEY,
    mission_id INTEGER REFERENCES missions(id),
    equipment_id INTEGER REFERENCES equipment(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

-- Trigger to update equipment status
CREATE OR REPLACE FUNCTION update_equipment_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE equipment
    SET status = 'assigned'
    WHERE id = NEW.equipment_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER equipment_assignment_trigger
AFTER INSERT ON mission_equipment
FOR EACH ROW
EXECUTE FUNCTION update_equipment_status();

-- Insert sample data
INSERT INTO locations (name, coordinates) VALUES
('Base Alpha', '40.7128,-74.0060'),
('Base Bravo', '34.0522,-118.2437');

INSERT INTO roles (name, description) VALUES
('Commander', 'Leads the mission'),
('Technician', 'Handles equipment');

INSERT INTO equipment (name, type, status) VALUES
('Radio', 'Communication', 'available'),
('GPS', 'Navigation', 'available');