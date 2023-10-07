CREATE DATABASE IF NOT EXISTS company_db;

USE company_db;

CREATE TABLE `Companies` (
  `ID` BIGINT,
  `CompanyName` VARCHAR(30),
  `Symbol` VARCHAR(5),
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Changelogs` (
  `CompanyID` BIGINT,
  `Date` DATETIME,
  `NewSymbol` VARCHAR(5),
  `OldSymbol` VARCHAR(5),
  `SymbolChanged` BOOLEAN,
  `NewName` VARCHAR(30),
  `OldName` VARCHAR(30),
  `NameChanged` BOOLEAN,
  PRIMARY KEY (`CompanyID`, `Date`),
  FOREIGN KEY (`CompanyID`) REFERENCES `Companies`(`ID`)
);

CREATE TABLE `Stock_Values` (
  `CompanyID` BIGINT,
  `Date` DATETIME,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  `Exchange` VARCHAR(20),
  PRIMARY KEY (`CompanyID`, `Date`),
  FOREIGN KEY (`CompanyID`) REFERENCES `Companies`(`ID`)
);

CREATE TABLE `Company_Statements` (
  `CompanyID` BIGINT,
  `Date` DATETIME,
  `Sector` VARCHAR(30),
  `Industry` VARCHAR(30),
  `FullTimeEmployees` DECIMAL,
  `MarketCap(Billions)` DECIMAL,
  `TrailingPE` DECIMAL,
  `ShortOfFloat` DECIMAL,
  `TraillingAnnualDividendYield` DECIMAL,
  `EnterpriseValue` DECIMAL,
  `NetIncome` DECIMAL,
  `Revenue` DECIMAL,
  `ReturnOnAssets` DECIMAL,
  `ReturnOnEquity` DECIMAL,
  PRIMARY KEY (`CompanyID`, `Date`),
  FOREIGN KEY (`CompanyID`) REFERENCES `Companies`(`ID`)
);