-- Filling tables with some data
INSERT INTO user (email, password, usrname)
VALUES 
('s4lv4dord@gmail.com', 'sha256$Zo1sPqXhu8aR4G9w$4fa51fce6799617ddf5eef13dee12bf339a3e607522699bf82eccfccaa6c22b4', 'sl4'), 
('camia2611@gmail', 'sha256$CwQn5Ty8vFVxPrGr$1c613c620628d19fce28ce75f8508e4bb56736f5e72e8bfde52ffc605f18b9be', 'cam');

INSERT INTO product (owner, name, sucursal, quantity, cost, price, expiry, qty_reserved, qr_barcode)
VALUES 
('s4lv4dord@gmail.com', 'salsa de tomate', 'suc1', 125, 50, 100, '2022-05-22', 0, '1234512345'),
('s4lv4dord@gmail.com', 'levadura puritas 10g','suc1', 100, 20, 50, '2022-05-22', 0, '1234512346'),
('s4lv4dord@gmail.com', 'pan duro', 'suc2', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('camia2611@hotmail.com', 'merluza 1kg', 'suc3', 93, 150, 350, '2022-05-19', 0, '1234512348');