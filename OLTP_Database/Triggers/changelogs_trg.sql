DELIMITER $$
CREATE TRIGGER changelog_companies_update_trg
AFTER INSERT ON Changelogs
FOR EACH ROW
BEGIN
	DECLARE temp INTEGER;
	SELECT COUNT(*) INTO temp FROM Companies WHERE ID = NEW.CompanyID;
	IF temp > 0 THEN
		IF (NEW.NameChanged = 1) AND (NEW.SymbolChanged = 1) THEN
			UPDATE Companies SET Symbol = NEW.NewSymbol, CompanyName = NEW.NewName WHERE ID = NEW.CompanyID;
		ELSEIF (NEW.NameChanged = 0) AND (NEW.SymbolChanged = 1) THEN
			UPDATE Companies SET Symbol = NEW.NewSymbol WHERE ID = NEW.CompanyID;
		ELSE
			UPDATE Companies SET CompanyName = NEW.NewName WHERE ID = NEW.CompanyID;
		END IF;
	ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'No associated record in Companies exists.';
	END IF;
END;
$$
DELIMITER ;