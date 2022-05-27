-- Create states table in DB with some data
CREATE DATABASE IF NOT EXISTS DB;
USE DB;

CREATE TABLE IF NOT EXISTS inventory ( 
    id INT AUTO_INCREMENT, 
    name VARCHAR(255) NOT NULL,
    sucursal VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    cost INT,
    price INT,
    expiry DATE,
    qty_reserved INT,
    qr_barcode VARCHAR(255),
    PRIMARY KEY (id)
);
-- we are not going to do a relationship with inventory
CREATE TABLE IF NOT EXISTS sucursal ( 
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);