CREATE DATABASE IF NOT EXISTS commodity_db;

USE commodity_db;

CREATE TABLE `Commodity_List` (
  `ID` BIGINT,
  `Name` VARCHAR(30),
  `Symbol` VARCHAR(5),
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Commodity_Values` (
  `CommodityID` BIGINT,
  `Date` DATETIME,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`CommodityID`, `Date`),
  FOREIGN KEY (`CommodityID`) REFERENCES `Commodity_List`(`ID`)
);