-- Filling tables with some data
-- INSERT INTO user (email, password, usrname)
-- VALUES 
-- ('s4lv4dord@gmail.com', 'sha256$Zo1sPqXhu8aR4G9w$4fa51fce6799617ddf5eef13dee12bf339a3e607522699bf82eccfccaa6c22b4', 'sl4'), 
-- ('camia2611@gmail.com', 'sha256$CwQn5Ty8vFVxPrGr$1c613c620628d19fce28ce75f8508e4bb56736f5e72e8bfde52ffc605f18b9be', 'cam');
INSERT INTO sucursal (name, owner) 
VALUES
 ('ptacarretas', 's4lv4dord@gmail.com'),
 ('pocitos', 's4lv4dord@gmail.com'),
 ('centro', 's4lv4dord@gmail.com'),
 ('perez castellanos', 'camia2611@gmail.com');

INSERT INTO product (owner, name, sucursal, quantity, cost, price, expiry, qty_reserved, qr_barcode)
VALUES 
('s4lv4dord@gmail.com', 'salsa de tomate', 'suc1', 125, 50, 100, '2022-05-22', 0, '1234512345'),
('s4lv4dord@gmail.com', 'levadura puritas 10g','suc1', 100, 20, 50, '2022-05-22', 0, '1234512346'),
('s4lv4dord@gmail.com', 'pan duro', 'suc2', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('camia2611@gmail.com', 'merluza 1kg', 'suc3', 93, 150, 350, '2022-05-19', 0, '1234512348'),
('s4lv4dord@gmail.com', 'a', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'b', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'c', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'd', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'e', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'f', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'g', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'h', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'i', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'i', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'k', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'l', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'm', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'n', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'o', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'p', 'pocitos', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'q', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'r', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 's', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 't', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'u', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'v', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'w', 'ptacarretas', 30, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'x', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'y', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'z', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ab', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ac', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ad', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'af', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ag', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ah', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ai', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'aj', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ak', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'al', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'am', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'an', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ao', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ap', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'aq', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ar', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'as', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'at', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'au', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'av', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'aw', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ax', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ay', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'az', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'ba', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'bb', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'bc', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347'),
('s4lv4dord@gmail.com', 'bd', 'ptacarretas', 25, 5, 45, '2022-05-21', 0, '1234512347');