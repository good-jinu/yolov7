DROP DATABASE IF EXISTS cap_db;
CREATE DATABASE cap_db default CHARACTER SET UTF8;
USE cap_db;
DROP TABLE IF EXISTS place_info;
CREATE TABLE place_info(
    PlaceID INT(11) PRIMARY KEY,
    Name VARCHAR(255),
    latitude DOUBLE(28, 25),
    longitude DOUBLE(28, 25),
    Class VARCHAR(255)
);

DROP TABLE IF EXISTS congestion;
CREATE TABLE congestion(
    PlaceID INT(11),
    FOREIGN KEY(PlaceID) REFERENCES hospital_info(HospitalID)
);