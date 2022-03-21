-- Database: `consumer`
--
CREATE DATABASE IF NOT EXISTS CONSUMER;
USE CONSUMER;

-- ---------------------------------------------------------------- --
--                     CONSUMER ACCOUNT TABLE                       --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CONSUMERACCOUNT_SEQ`
--
DROP TABLE IF EXISTS CONSUMERACCOUNT_SEQ;

CREATE TABLE CONSUMERACCOUNT_SEQ
(
	CONSUMERID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CONSUMERACCOUNT` --
--
DROP TABLE IF EXISTS CONSUMERACCOUNT;

CREATE TABLE IF NOT EXISTS CONSUMERACCOUNT (
	CONSUMERID varchar(64) NOT NULL,
	USERNAME varchar(64) NOT NULL,
	PASSWORD varchar(64) NOT NULL,
	TELEGRAM varchar(64) NOT NULL,
	PRIMARY KEY (CONSUMERID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATORACCOUNT`
--

DELIMITER $$
CREATE TRIGGER tg_consumeraccount_insert
BEFORE INSERT ON CONSUMERACCOUNT
FOR EACH ROW
BEGIN
	INSERT INTO CONSUMERACCOUNT_SEQ VALUES (NULL);
	SET NEW.CONSUMERID = CONCAT('CON', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into CONSUMERACCOUNT -- 
--

INSERT INTO CONSUMERACCOUNT(USERNAME,PASSWORD,TELEGRAM) 
VALUES ('imnew', 'pass123','@tinklebell'),
('logi', 'pass123','@hutthutt');