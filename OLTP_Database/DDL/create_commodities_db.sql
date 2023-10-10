CREATE DATABASE IF NOT EXISTS commodity_db;

USE commodity_db;

CREATE TABLE `Commodity_List` (
  `ID` BIGINT,
  `Name` VARCHAR(30) NOT NULL,
  `Symbol` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Commodity_Values` (
  `CommodityID` BIGINT,
  `Date` DATETIME,
  `Open` DECIMAL(12,2),
  `High` DECIMAL(12,2),
  `Low` DECIMAL(12,2),
  `Close` DECIMAL(12,2),
  `Volume` DECIMAL(12,2),
  PRIMARY KEY (`CommodityID`, `Date`),
  FOREIGN KEY (`CommodityID`) REFERENCES `Commodity_List`(`ID`)
);