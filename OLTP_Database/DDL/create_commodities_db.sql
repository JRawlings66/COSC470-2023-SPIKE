CREATE DATABASE IF NOT EXISTS commodity_db;

USE commodity_db;

CREATE TABLE `commodity_list` (
  `ID ` INTEGER,
  `Name` VARCHAR(30),
  `Symbol` VARCHAR(5),
  PRIMARY KEY (`ID `)
);

CREATE TABLE `commodity_values` (
  `CommodityID ` INTEGER,
  `Date` DATETIME,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`CommodityID `, `Date`)
);
