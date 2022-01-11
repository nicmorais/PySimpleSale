CREATE TABLE unit (unit_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, abbreviation TEXT)

CREATE TABLE product (product_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, cost REAL NOT NULL, quantity REAL NOT NULL, barcode TEXT UNIQUE, unit_id INTEGER NOT NULL, FOREIGN KEY (unit_id) REFERENCES unit(unit_id));

CREATE TABLE country (country_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, code TEXT NOT NULL);

CREATE TABLE state (state_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, code TEXT, country_id INTEGER NOT NULL, FOREIGN KEY(country_id) REFERENCES country(country_id));

CREATE TABLE city (city_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, state_id INTEGER NOT NULL, FOREIGN KEY(state_id) REFERENCES state(state_id));

CREATE TABLE customer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address_line1 TEXT, address_line2 TEXT, zipcode TEXT, email TEXT UNIQUE, phone_number INTEGER UNIQUE, city_id INTEGER, FOREIGN KEY(city_id) REFERENCES city(city_id))

CREATE TABLE supplier (supplier_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address_line1 TEXT, address_line2 TEXT, city_id INTEGER, email TEXT, phone_number INTEGER, FOREIGN KEY(city_id) REFERENCES city(city_id))

CREATE TABLE sale (sale_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, amount REAL NOT NULL, discount REAL NOT NULL, shipping REAL NOT NULL, datetime TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id))

CREATE TABLE sale_product (sale_product_id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL NOT NULL, quantity REAL NOT NULL, product_id INTEGER NOT NULL, sale_id INTEGER NOT NULL, FOREIGN KEY (product_id) REFERENCES product(product_id), FOREIGN KEY (sale_id) REFERENCES sale(sale_id))

CREATE TABLE purchase (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_id INTEGER NOT NULL, amount REAL NOT NULL, discount REAL NOT NULL, shipping REAL NOT NULL, datetime TEXT NOT NULL, FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id))

CREATE VIEW sale_view AS SELECT sale_id, name, amount, datetime FROM sale JOIN customer USING(customer_id);

CREATE VIEW purchase_view AS SELECT purchase_id, name, amount, datetime FROM purchase JOIN supplier USING(supplier_id);
