CREATE TABLE IF NOT EXISTS location(
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    active ENUM('True', 'False') NOT NULL,
    PRIMARY KEY (country, city)
) ENGINE=innodb; 


INSERT INTO location (country, city, active) values ('AG', 'San Juan', 'False');
INSERT INTO location (country, city, active) values ('PA', 'Ciudad De Panama', 'False');
INSERT INTO location (country, city, active) values ('PG', 'Puerto De Moresby', 'False');
INSERT INTO location (country, city, active) values ('PK', 'Islamabad', 'False');
INSERT INTO location (country, city, active) values ('PY', 'Asuncion', 'False');
INSERT INTO location (country, city, active) values ('TT', 'Puerto De España', 'False');

