-- Filling tables with some data
INSERT INTO sucursal (name)
VALUES 
('sucursal1'), ('sucursal2'), ('sucursal3');

INSERT INTO inventory (name, sucursal, quantity, cost, price, expiry, qty_reserved, qr_barcode)
VALUES 
('salsa de tomate', 'suc1', 125, 50, 100, '2022-05-22', 0, '1234512345'),
('levadura puritas 10g','suc1', 100, 20, 50, '2022-05-22', 0, '1234512346'),
('pan duro', 'suc2', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('merluza 1kg', 'suc3', 93, 150, 350, '2022-05-19', 0, '1234512348');