CREATE DATABASE IF NOT EXISTS index_db;

USE index_db;

CREATE TABLE `NASDAQ_index` (
  `Date` DATETIME,
  `Ticker` VARCHAR(5),
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`Date`)
);

CREATE TABLE `DowJones_index` (
  `Date` DATETIME,
  `Ticker` VARCHAR(5),
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`Date`)
);

CREATE TABLE `SNP500_index` (
  `Date` DATETIME,
  `Ticker` VARCHAR(5),
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`Date`)
);