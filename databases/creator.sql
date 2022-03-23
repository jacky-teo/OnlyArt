-- Database: `creator`
--
CREATE DATABASE IF NOT EXISTS CREATOR;
USE CREATOR;

-- ---------------------------------------------------------------- --
--                     CREATOR ACCOUNT TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CREATORACCOUNT_SEQ` --
--
DROP TABLE IF EXISTS CREATORACCOUNT_SEQ;
CREATE TABLE CREATORACCOUNT_SEQ
(
	CREATORID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CREATORACCOUNT` --
--
DROP TABLE IF EXISTS CREATORACCOUNT;
CREATE TABLE IF NOT EXISTS CREATORACCOUNT (
	CREATORID varchar(64) NOT NULL,
	USERNAME varchar(64) NOT NULL,
	PASSWORD varchar(64) NOT NULL,
	EMAIL varchar(64) NOT NULL,
	PRICE decimal(10,2) NOT NULL,
	PRIMARY KEY (CREATORID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATORACCOUNT` --
--

DELIMITER $$
CREATE TRIGGER tg_creatoraccount_insert
BEFORE INSERT ON CREATORACCOUNT
FOR EACH ROW
BEGIN
	INSERT INTO CREATORACCOUNT_SEQ VALUES (NULL);
	SET NEW.CREATORID = CONCAT('CR', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into `CREATORACCOUNT` --
--
INSERT INTO CREATORACCOUNT(USERNAME,PASSWORD,EMAIL,PRICE) 
VALUES 
('jackyteo', 'pass123', 'sb-go47cv14389012@business.example.com',100.00),
('notJacky', 'pass123', 'jackyteojianqi@gmail.com',233.50);


