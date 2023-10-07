CREATE DATABASE IF NOT EXISTS data_warehouse;

USE data_warehouse;

CREATE TABLE `dim_stock` (
  `StockKey` INT,
  `CompanyKey` INT,
  `ExchangeKey` INT,
  `Symbol` VARCHAR(5),
  PRIMARY KEY (`StockKey`)
);

CREATE TABLE `fact_commodities` (
  `CommoditiesKey` INT,
  `DateKey` DATETIME,
  `Name` VARCHAR(30),
  `Symbol` VARCHAR(5),
  `Field` DECIMAL,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`CommoditiesKey`)
);

CREATE TABLE `fact_index` (
  `indexSymboleKey` INT,
  `Date_key` INT,
  `IndexKey` Type,
  `Open` DECIMAL,
  `HIGH` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`indexSymboleKey`)
);

CREATE TABLE `dim_date` (
  `DateKey` INT,
  `Date` DATETIME,
  `Year` INT,
  `Month` INT,
  `DayInMonth` INT,
  `DayInWeek` INT,
  `DayInWeekName` VARCHAR(10) ,
  `Quarter` INT,
  `QuarterName` VARCHAR(2) ,
  `MonthName` VARCHAR(3),
  `DayInYear` INT,
  PRIMARY KEY (`DateKey`),
  FOREIGN KEY (`DateKey`) REFERENCES `fact_commodities`(`DateKey`),
  FOREIGN KEY (`DateKey`) REFERENCES `fact_index`(`Date_key`)
);

CREATE TABLE `fact_stock_market` (
  `SymbolKey` INT,
  `DateKey` INT,
  `StockKey` INT,
  `ExchangeKey` DECIMAL,
  `DayHigh` DECIMAL,
  `DayLow` DECIMAL,
  `Day Close` DECIMAL,
  `PRICE` DECIMAL,
  `Changes Percentage` DECIMAL,
  `Change` DECIMAL,
  `Open` DECIMAL,
  PRIMARY KEY (`SymbolKey`),
  FOREIGN KEY (`StockKey`) REFERENCES `dim_stock`(`StockKey`),
  FOREIGN KEY (`DateKey`) REFERENCES `dim_date`(`DateKey`)
);

CREATE TABLE `IndustryToCompanyBridgeTable` (
  `IndexKey` INT,
  `IndustryKey` INT,
  `CompanyKey` INT,
  `IndexTicker` VARCHAR(5),
  PRIMARY KEY (`IndexKey`)
);

CREATE TABLE `dim_industry` (
  `IndustryKey` INT,
  `IndexKey` INT,
  `Industry` VARCHAR(30),
  `Sector` VARCHAR(30),
  PRIMARY KEY (`IndustryKey`),
  FOREIGN KEY (`IndustryKey`) REFERENCES `IndustryToCompanyBridgeTable`(`IndexKey`)
);

CREATE TABLE `dim_company` (
  `CompanyInfoKey` INT,
  `IndexKey` INT,
  `Name` BOOL,
  `Name` VARCHAR(30),
  `MarketCap(Billions)` DECIMAL,
  `TrailingPE` DECIMAL,
  `ShortOfFloat` DECIMAL,
  `TrailingAnnualDividendYield` DECIMAL,
  `EnterpriseValue` DECIMAL,
  `NetIncome` DECIMAL,
  `Revenue` DECIMAL,
  `ReturnOnAssets` DECIMAL,
  `ReturnOnEquity` DECIMAL,
  `FullTimeEmployees` DECIMAL,
  `Sector` VARCHAR(20),
  `Industry` VARCHAR(20),
  PRIMARY KEY (`CompanyInfoKey`),
  FOREIGN KEY (`CompanyInfoKey`) REFERENCES `dim_stock`(`CompanyKey`),
  FOREIGN KEY (`IndexKey`) REFERENCES `IndustryToCompanyBridgeTable`(`IndexKey`)
);

CREATE TABLE `Stock exchange` (
  `IndexKey` INT,
  `CompanyinfoKey` INT,
  `name` VARCHAR(20),
  PRIMARY KEY (`IndexKey`),
  FOREIGN KEY (`IndexKey`) REFERENCES `dim_stock`(`ExchangeKey`)
);

CREATE TABLE `exchange_company_bridge_table` (
  `iterator` INT,
  `companyKey` VARCHAR(5),
  `exchangeKey` Type,
  PRIMARY KEY (`iterator`)
);

CREATE TABLE `fact_bond` (
  `Bond_Key` INT,
  `Date` DATETYPE,
  `month_1` Float,
  `Month_2` Float,
  `Month_3` Float,
  `Month_6` Float,
  `Year_1` Float,
  `Year_2` Float,
  `Year_3` Float,
  `Year_5` Float,
  `Year_7` Float,
  `Year_10 ` Type,
  `Year_20` Float,
  PRIMARY KEY (`Bond_Key`)
);

CREATE TABLE `dim_index_table` (
  `IndexKey` INT,
  `IndexTicker` VARCHAR(5),
  `Name` VARCHAR(20),
  PRIMARY KEY (`IndexKey`),
  FOREIGN KEY (`IndexKey`) REFERENCES `fact_index`(`IndexKey`)
);

