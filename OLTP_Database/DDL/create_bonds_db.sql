CREATE DATABASE IF NOT EXISTS bonds_db;

USE bonds_db;

CREATE TABLE `Bonds` (
  `Date` DATETIME,
  `BondDuration` VARCHAR(10),
  `Rate` DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (`Date`, `BondDuration`)
);