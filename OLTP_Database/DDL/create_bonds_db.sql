CREATE DATABASE IF NOT EXISTS bonds_db;

USE bonds_db;

CREATE TABLE `2yr_bonds` (
  `Date` DATETIME,
  `Rate` DECIMAL,
  PRIMARY KEY (`Date`)
);

CREATE TABLE `5yr_bonds` (
  `Date` DATETIME,
  `Rate` DECIMAL,
  PRIMARY KEY (`Date`)
);

CREATE TABLE `7yr_bonds` (
  `Date` DATETIME,
  `Rate` DECIMAL,
  PRIMARY KEY (`Date`)
);