CREATE DATABASE IF NOT EXISTS index_db;

USE index_db;

CREATE TABLE `Indices` (
  `ID` BIGINT,
  `Symbol` VARCHAR(10),
  `Name` VARCHAR(20),
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Index_Values` (
  `Date` DATETIME,
  `IndexID` BIGINT,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`Date`, `IndexID`),
  FOREIGN KEY (`IndexID`) REFERENCES `Indices`(`ID`)
);