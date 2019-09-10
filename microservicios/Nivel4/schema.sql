CREATE TABLE IF NOT EXISTS location(
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    active ENUM('True', 'False') NOT NULL,
    PRIMARY KEY (country, city)
) ENGINE=innodb DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS product(
    sku varchar (7) NOT NULL,
    description varchar(100) NOT NULL,
    price decimal(6,2) NOT NULL,
    PRIMARY KEY (sku)
) ENGINE=innodb DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS rules(
    id INT NOT NULL AUTO_INCREMENT,
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    sku varchar(7) NOT NULL,
    min_condition int(3) NOT NULL,
    max_condition int(3) NOT NULL,
    variation DECIMAL(2,1) NOT NULL,
    PRIMARY KEY (id), index (country), index(city),
    FOREIGN KEY (sku) REFERENCES product (sku),
    foreign key (country, city) REFERENCES location (country, city)
) ENGINE = innodb;

INSERT INTO product (sku, description, price) VALUES ('AZ00001', 'Paraguas de señora estampado', 10.0);
INSERT INTO product (sku, description, price) VALUES ('AZ00002', 'Helado de sabor fresa', 10.0);

INSERT INTO rules values(NULL, 'NI', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO rules values(NULL, 'NI', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO rules values(NULL, 'NI', 'Managua', 'AZ00001', 800, 804, 0.5);
INSERT INTO rules values(NULL, 'NI', 'Managua', 'AZ00002', 800, 804, 1.5);
INSERT INTO rules values(NULL, 'NI', 'Leon', 'AZ00001', 500, 599, 1.5);
INSERT INTO rules values(NULL, 'NI', 'Leon', 'AZ00002', 500, 599, 0.5);
INSERT INTO rules values(NULL, 'NI', 'Leon', 'AZ00001', 800, 804, 0.5);
INSERT INTO rules values(NULL, 'NI', 'Leon', 'AZ00002', 800, 804, 1.5);

