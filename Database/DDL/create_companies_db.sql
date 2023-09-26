

CREATE TABLE `companies` (
  `ID` INTEGER,
  `CompanyName` VARCHAR(30),
  `StockID` INTEGER,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `stocks` (
  `ID` INTEGER,
  `Symbol` VARCHAR(5),
  PRIMARY KEY (`ID`)
);

CREATE TABLE `changelogs` (
  `CompanyID` INTEGER,
  `StockID` INTEGER,
  `Date` DATETIME,
  `New_Symbol` VARCHAR(5),
  `Old_Symbol` VARCHAR(5),
  `Symbol_Changed` BOOLEAN,
  `New_Name` VARCHAR(30),
  `Old_Name` VARCHAR(30),
  `Name_Changed` BOOLEAN,
  PRIMARY KEY (`CompanyID`, `StockID`),
  FOREIGN KEY (`CompanyID`) REFERENCES `Companies`(`ID`),
  FOREIGN KEY (`StockID`) REFERENCES `Stocks`(`ID`),
  KEY `CK` (`Date`)
);

CREATE TABLE `stock_Values` (
  `StockID` INTEGER,
  `Date` DATETIME,
  `Open` DECIMAL,
  `High` DECIMAL,
  `Low` DECIMAL,
  `Close` DECIMAL,
  `Volume` DECIMAL,
  PRIMARY KEY (`StockID`, `Date`),
  FOREIGN KEY (`StockID`) REFERENCES `Stocks`(`ID`)
);

CREATE TABLE `company_statements` (
  `CompanyID` INTEGER,
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