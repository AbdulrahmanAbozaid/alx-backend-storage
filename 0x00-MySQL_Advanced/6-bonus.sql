-- 6-bonus.sql
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    -- Check if the project already exists, if not create it
    DECLARE project_id INT;
    
    -- Select project_id based on project_name
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name
    LIMIT 1;
    
    -- If no project found, create a new one
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    -- Add the correction for the user and the project
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END//

DELIMITER ;
