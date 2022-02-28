CREATE TABLE unit (unit_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, abbreviation TEXT UNIQUE NOT NULL)

CREATE TABLE product (product_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, cost REAL NOT NULL, quantity REAL NOT NULL, barcode TEXT UNIQUE, unit_id INTEGER NOT NULL, FOREIGN KEY (unit_id) REFERENCES unit(unit_id) ON DELETE RESTRICT)

CREATE TABLE country (country_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, code TEXT NOT NULL);

CREATE TABLE state (state_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, code TEXT, country_id INTEGER NOT NULL, FOREIGN KEY(country_id) REFERENCES country(country_id));

CREATE TABLE city (city_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, state_id INTEGER NOT NULL, FOREIGN KEY(state_id) REFERENCES state(state_id));

CREATE TABLE customer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address_line1 TEXT, address_line2 TEXT, zipcode TEXT, email TEXT UNIQUE, phone_number INTEGER UNIQUE, city_id INTEGER, FOREIGN KEY(city_id) REFERENCES city(city_id))

CREATE TABLE supplier (supplier_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address_line1 TEXT, address_line2 TEXT, city_id INTEGER, email TEXT, phone_number TEXT, FOREIGN KEY(city_id) REFERENCES city(city_id))

CREATE TABLE sale (sale_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, amount REAL NOT NULL, discount REAL NOT NULL, shipping REAL NOT NULL, datetime TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id)) ON DELETE RESTRICT

CREATE TABLE sale_product (sale_product_id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL NOT NULL, quantity REAL NOT NULL, product_id INTEGER NOT NULL, sale_id INTEGER NOT NULL, FOREIGN KEY (product_id) REFERENCES product(product_id), FOREIGN KEY (sale_id) REFERENCES sale(sale_id))

CREATE TABLE purchase (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_id INTEGER NOT NULL, amount REAL NOT NULL, discount REAL NOT NULL, shipping REAL NOT NULL, datetime TEXT NOT NULL, FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id))

CREATE TABLE purchase_product (purchase_product_id INTEGER PRIMARY KEY AUTOINCREMENT, sale_price REAL NOT NULL, cost REAL NOT NULL, quantity REAL NOT NULL, product_id INTEGER NOT NULL, purchase_id INTEGER NOT NULL, FOREIGN KEY (product_id) REFERENCES product(product_id), FOREIGN KEY (purchase_id) REFERENCES purchase(purchase_id))

CREATE VIEW sale_view AS SELECT sale_id, name, amount, datetime FROM sale JOIN customer USING(customer_id);

CREATE VIEW purchase_view AS SELECT purchase_id, name, amount, datetime FROM purchase JOIN supplier USING(supplier_id);

CREATE TRIGGER update_product_quantity_after_insert_sale_product_tg AFTER INSERT ON sale_product BEGIN UPDATE product SET quantity = quantity - new.quantity WHERE product_id = new.product_id; END;

CREATE TRIGGER update_product_quantity_before_update_sale_product_tg BEFORE UPDATE ON sale_product WHEN old.quantity <> new.quantity BEGIN UPDATE product SET quantity = quantity + (new.quantity - old.quantity) WHERE product_id = new.product_id; END;

CREATE TRIGGER update_product_quantity_after_delete_sale_product_tg AFTER DELETE ON sale_product BEGIN UPDATE product SET quantity = quantity + old.quantity WHERE product_id = old.product_id; END;

CREATE TRIGGER update_product_quantity_after_insert_purchase_product_tg AFTER INSERT ON purchase_product BEGIN UPDATE product SET quantity = quantity + new.quantity, price = new.sale_price, cost = new.cost WHERE product_id = new.product_id; END;

CREATE TRIGGER update_product_purchase_before_update_sale_product_tg BEFORE UPDATE ON purchase_product WHEN old.quantity <> new.quantity BEGIN UPDATE product SET quantity = quantity + (new.quantity - old.quantity) WHERE product_id = new.product_id; END;

CREATE TRIGGER update_product_quantity_after_delete_purchase_product_tg AFTER DELETE ON purchase_product BEGIN UPDATE product SET quantity = quantity - old.quantity WHERE product_id = old.product_id; END;
