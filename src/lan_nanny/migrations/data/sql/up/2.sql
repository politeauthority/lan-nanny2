--- 
--- Migration 2
--- Lan Nanny Core tables
---
---
--- Create devices
---
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR,
    vendor_id INTEGER,
    ip VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    last_port_scan TIMESTAMP,
    port_scan_lock BOOLEAN,
    identified BOOLEAN,
    hide BOOLEAN DEFAULT False,
    icon VARCHAR,
    deleted BOOLEAN DEFAULT False
);

CREATE TABLE IF NOT EXISTS device_macs (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    address VARCHAR UNIQUE,
    last_ip VARCHAR,
    device_id INTEGER,
    vendor_id INTEGER,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    hide BOOLEAN DEFAULT False,
    last_port_scan TIMESTAMP,
    port_scan_lock BOOLEAN,
    host_names VARCHAR,
    kind_id INTEGER,
    identified BOOLEAN,
    deleted BOOLEAN DEFAULT False,
    port_scan_enabled BOOLEAN default True
);

CREATE TABLE IF NOT EXISTS device_ports (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_id INTEGER,
    device_mac_id INTEGER NOT NULL,
    last_scan_port_id INTEGER NOT NULL,
    state VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    protocol VARCHAR,
    port_num INTEGER NOT NULL,
    UNIQUE (device_mac_id, protocol, port_num)
);

CREATE TABLE IF NOT EXISTS device_kinds (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR UNIQUE,
    icon VARCHAR
);

CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS scan_hosts (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_agent VARCHAR NOT NULL,
    scan_type VARCHAR NOT NULL,
    hosts_found INTEGER NOT NULL,
    scan_command VARCHAR,
    scan_time INTEGER,
    raw_data TEXT
);

CREATE TABLE IF NOT EXISTS scan_host_results (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_host_id INTEGER NOT NULL,
    device_mac_id INTEGER NOT NULL,
    device_id INTEGER
);

CREATE TABLE IF NOT EXISTS scan_ports (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_agent VARCHAR NOT NULL,
    scan_type VARCHAR NOT NULL,
    device_id INTEGER,
    device_mac_id INTEGER NOT NULL,
    elapsed_time NUMERIC,
    ports_found INTEGER,
    scan_command VARCHAR,
    scan_time TIMESTAMP,
    scan_success BOOLEAN,
    raw_data TEXT
);


-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/2.sql
