BEGIN;

/*
  SchwabEats PostgreSQL schema

  This schema is designed around:
  - the current frontend ordering flow
  - the broader assignment requirements in the project document

  Core areas covered:
  - employees, campuses, delivery zones, and eligibility
  - vendors, contracts, approvals, and operating hours
  - menus, items, allergens, and customization options
  - orders, order items, status history, and modification history
  - cutoff rules, blackout dates, pickup confirmation, and incidents
  - seed data that matches the current frontend ordering page
*/

-- Stores each Charles Schwab office/campus that can use SchwabEats.
-- Other tables connect back to campuses so ordering rules, vendors, and delivery areas can be campus-specific.
CREATE TABLE IF NOT EXISTS campuses (
    campus_id BIGSERIAL PRIMARY KEY,
    campus_code VARCHAR(20) NOT NULL UNIQUE,
    campus_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    timezone_name VARCHAR(64) NOT NULL DEFAULT 'America/Chicago',
    is_participating BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Stores physical buildings on a campus.
-- Delivery zones point to buildings so employees can choose the correct pickup or delivery location.
CREATE TABLE IF NOT EXISTS buildings (
    building_id BIGSERIAL PRIMARY KEY,
    campus_id BIGINT NOT NULL REFERENCES campuses(campus_id),
    building_code VARCHAR(30) NOT NULL,
    building_name VARCHAR(150) NOT NULL,
    street_address_1 VARCHAR(150),
    street_address_2 VARCHAR(150),
    city VARCHAR(100),
    state_code CHAR(2),
    postal_code VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (campus_id, building_code)
);

-- Stores pickup or delivery areas inside a campus/building.
-- This is how the system knows where an order should be delivered or picked up.
CREATE TABLE IF NOT EXISTS delivery_zones (
    delivery_zone_id BIGSERIAL PRIMARY KEY,
    campus_id BIGINT NOT NULL REFERENCES campuses(campus_id),
    building_id BIGINT REFERENCES buildings(building_id),
    zone_code VARCHAR(30) NOT NULL,
    zone_name VARCHAR(150) NOT NULL,
    floor_label VARCHAR(30),
    room_label VARCHAR(30),
    facilities_coordinator_name VARCHAR(150),
    facilities_coordinator_email VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (campus_id, zone_code)
);

-- Stores employee departments such as Engineering, HR, or Finance.
-- Employees reference this table so reporting and eligibility can be grouped by department.
CREATE TABLE IF NOT EXISTS departments (
    department_id BIGSERIAL PRIMARY KEY,
    department_code VARCHAR(30) NOT NULL UNIQUE,
    department_name VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Stores employee profile and eligibility information.
-- This controls who can order, where they are located, and whether they qualify for SchwabEats access.
CREATE TABLE IF NOT EXISTS employees (
    employee_id BIGSERIAL PRIMARY KEY,
    employee_number VARCHAR(30) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department_id BIGINT REFERENCES departments(department_id),
    campus_id BIGINT REFERENCES campuses(campus_id),
    default_delivery_zone_id BIGINT REFERENCES delivery_zones(delivery_zone_id),
    employment_type VARCHAR(30) NOT NULL
        CHECK (employment_type IN ('full_time', 'part_time', 'intern', 'contractor')),
    weekly_hours NUMERIC(5,2),
    role_name VARCHAR(100) NOT NULL DEFAULT 'employee',
    is_department_head_approved BOOLEAN NOT NULL DEFAULT FALSE,
    has_active_access BOOLEAN NOT NULL DEFAULT TRUE,
    hr_status VARCHAR(30) NOT NULL DEFAULT 'active'
        CHECK (hr_status IN ('active', 'leave', 'terminated', 'inactive')),
    remote_status VARCHAR(20) NOT NULL DEFAULT 'onsite'
        CHECK (remote_status IN ('onsite', 'hybrid', 'remote')),
    has_medical_allergy_flags BOOLEAN NOT NULL DEFAULT FALSE,
    has_religious_dietary_flags BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Stores saved pickup/delivery locations for each employee.
-- This lets an employee have a default location and optional alternate locations.
CREATE TABLE IF NOT EXISTS employee_delivery_locations (
    employee_delivery_location_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    delivery_zone_id BIGINT NOT NULL REFERENCES delivery_zones(delivery_zone_id),
    location_label VARCHAR(100) NOT NULL,
    instructions TEXT,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (employee_id, location_label)
);

-- Stores allergies, religious dietary needs, and preferences for employees.
-- This supports safer ordering and lets the app warn or filter menu items later.
CREATE TABLE IF NOT EXISTS employee_dietary_restrictions (
    employee_dietary_restriction_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    restriction_type VARCHAR(30) NOT NULL
        CHECK (restriction_type IN ('allergy', 'religious', 'preference')),
    restriction_code VARCHAR(50) NOT NULL,
    restriction_label VARCHAR(100) NOT NULL,
    source_system VARCHAR(50) NOT NULL DEFAULT 'manual',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (employee_id, restriction_type, restriction_code)
);

-- Stores restaurant/vendor records.
-- This includes approval status, cuisine type, contact info, images, and whether the vendor can accept orders.
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id BIGSERIAL PRIMARY KEY,
    vendor_code VARCHAR(30) NOT NULL UNIQUE,
    legal_name VARCHAR(150) NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(30),
    tax_id VARCHAR(50),
    cuisine_type VARCHAR(100),
    certification_status VARCHAR(30) NOT NULL DEFAULT 'pending'
        CHECK (certification_status IN ('pending', 'approved', 'rejected')),
    vendor_status VARCHAR(30) NOT NULL DEFAULT 'draft'
        CHECK (vendor_status IN ('draft', 'pending', 'active', 'paused', 'suspended', 'inactive')),
    delivery_radius_miles NUMERIC(6,2),
    pause_incoming_orders BOOLEAN NOT NULL DEFAULT FALSE,
    image_url TEXT,
    promo_banner_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Stores people to contact for each vendor.
-- Useful for operations, support, contract questions, and delivery issues.
CREATE TABLE IF NOT EXISTS vendor_contacts (
    vendor_contact_id BIGSERIAL PRIMARY KEY,
    vendor_id BIGINT NOT NULL REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    contact_name VARCHAR(150) NOT NULL,
    contact_role VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(30),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);