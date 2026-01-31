CREATE DATABASE IF NOT EXISTS entity_service_provider;

USE entity_service_provider;

CREATE TABLE entities (
    entity_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_name VARCHAR(255) NOT NULL
);

CREATE TABLE service_providers (
    provider_id INT AUTO_INCREMENT PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    provider_type ENUM('Auditor', 'Administrator', 'Custodian') NOT NULL
);

CREATE TABLE entity_provider_relationships (
    relationship_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT,
    provider_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id),
    FOREIGN KEY (provider_id) REFERENCES service_providers(provider_id)
);

SHOW DATABASES;
USE entity_service_provider;
SHOW TABLES;
USE entity_service_provider;

SELECT COUNT(*) FROM entities;


USE entity_service_provider;

USE entity_service_provider;

TRUNCATE TABLE entity_provider_relationships;
TRUNCATE TABLE service_providers;
TRUNCATE TABLE entities;
USE entity_service_provider;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE entity_provider_relationships;
TRUNCATE TABLE service_providers;
TRUNCATE TABLE entities;

#SET FOREIGN_KEY_CHECKS = 1;


SELECT COUNT(*) FROM entities;
SELECT COUNT(*) FROM service_providers;
SELECT COUNT(*) FROM entity_provider_relationships;

SELECT MIN(entity_id), MAX(entity_id) FROM entities;
select count(entity_id) from entity_provider_relationships;



SELECT COUNT(*) FROM (
    SELECT 
    e.entity_id,
    e.entity_name,
    GROUP_CONCAT(DISTINCT sp.provider_type) AS existing_provider_types
FROM entities e
LEFT JOIN entity_provider_relationships r
    ON e.entity_id = r.entity_id
LEFT JOIN service_providers sp
    ON r.provider_id = sp.provider_id
GROUP BY e.entity_id, e.entity_name
HAVING 
    SUM(sp.provider_type = 'Auditor') = 0
    OR SUM(sp.provider_type = 'Custodian') = 0
    OR SUM(sp.provider_type = 'Administrator') = 0
) AS missing_entities;
USE entity_service_provider;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE entity_provider_relationships;
TRUNCATE TABLE service_providers;
TRUNCATE TABLE entities;

SET FOREIGN_KEY_CHECKS = 1;

use entity_service_provider;
SELECT
    e.entity_id,
    e.entity_name,
    sp.provider_type,
    COUNT(*) AS active_provider_count
FROM entity_provider_relationships r
JOIN entities e
    ON r.entity_id = e.entity_id
JOIN service_providers sp
    ON r.provider_id = sp.provider_id
WHERE r.end_date >= CURDATE()
GROUP BY e.entity_id, e.entity_name, sp.provider_type
HAVING COUNT(*) > 1;



SELECT COUNT(DISTINCT entity_id) AS affected_entities
FROM (
    SELECT
        e.entity_id
    FROM entity_provider_relationships r
    JOIN entities e
        ON r.entity_id = e.entity_id
    JOIN service_providers sp
        ON r.provider_id = sp.provider_id
    WHERE r.end_date >= CURDATE()
    GROUP BY e.entity_id, sp.provider_type
    HAVING COUNT(*) > 1
) t;



USE entity_service_provider;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE entity_provider_relationships;
TRUNCATE TABLE service_providers;
TRUNCATE TABLE entities;

SET FOREIGN_KEY_CHECKS = 1;

