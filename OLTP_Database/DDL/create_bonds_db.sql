CREATE DATABASE IF NOT EXISTS bonds_db;

USE bonds_db;

CREATE TABLE `Bonds` (
  `Date` DATETIME,
  `BondDuration` VARCHAR(10),
  `Rate` DECIMAL,
  PRIMARY KEY (`Date`, `BondDuration`)
);