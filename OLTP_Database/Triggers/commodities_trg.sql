DELIMITER $$
CREATE TRIGGER commodity_list_id_gen_trg
BEFORE INSERT ON Commodity_List
FOR EACH ROW
BEGIN
	DECLARE new_id BIGINT;
	DECLARE temp INTEGER;
	DECLARE valid INTEGER;
    SET new_id = UUID_SHORT();
    SET valid = 1;
	SELECT COUNT(*) INTO temp FROM Commodity_List WHERE Symbol = NEW.Symbol;
	IF (temp = 0) THEN
    	WHILE (valid = 1) DO
        	SELECT COUNT(*) INTO temp FROM Commodity_List WHERE ID = new_id;
        	IF (temp = 1) THEN
            	SET new_id = UUID_SHORT();
   		 ELSE
   		 	SET valid = 0;
        	END IF;
    	END WHILE;
    ELSE
    	SIGNAL SQLSTATE '45000'
   	 SET MESSAGE_TEXT = 'A record for this stock already exists.';
    END IF;
	SET NEW.ID = new_id;
END;
$$
DELIMITER ;