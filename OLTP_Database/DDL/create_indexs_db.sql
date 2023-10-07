CREATE DATABASE IF NOT EXISTS index_db;

USE index_db;

CREATE TABLE `Indices` (
  `ID` BIGINT,
  `Symbol` VARCHAR(10) NOT NULL,
  `Name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Index_Values` (
  `Date` DATETIME,
  `IndexID` BIGINT,
  `Open` DECIMAL(12,2),
  `High` DECIMAL(12,2),
  `Low` DECIMAL(12,2),
  `Close` DECIMAL(12,2),
  `Volume` DECIMAL(12,2),
  PRIMARY KEY (`Date`, `IndexID`),
  FOREIGN KEY (`IndexID`) REFERENCES `Indices`(`ID`)
);