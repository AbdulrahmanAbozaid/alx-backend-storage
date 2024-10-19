-- 4. Buy buy buy
-- This script creates a trigger to update the item quantity after a new order is added
DELIMITER //

CREATE TRIGGER update_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END//

DELIMITER ;
