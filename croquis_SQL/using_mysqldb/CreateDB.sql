-- Create states table in DB with some data
CREATE DATABASE IF NOT EXISTS DB;
USE DB;
CREATE TABLE IF NOT EXISTS Inventory ( 
    id VARCHAR(64) NOT NULL, 
    name VARCHAR(256) NOT NULL,
    price int,
    qr_barcode VARCHAR(256),
    PRIMARY KEY (id)
);
