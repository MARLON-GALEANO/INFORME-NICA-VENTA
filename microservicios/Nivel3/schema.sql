CREATE TABLE IF NOT EXISTS location(
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    active ENUM('True', 'False') NOT NULL,
    PRIMARY KEY (country, city)
) ENGINE=innodb;


