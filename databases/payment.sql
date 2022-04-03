-- Database: `payment`
--
CREATE DATABASE IF NOT EXISTS PAYMENT;
USE PAYMENT;

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
('jackyteo', 'pass123', 'jacky.teo.2020@smu.edu.sg',100.00),
('notJacky', 'pass123', 'jackyteojianqi@gmail.com',233.50);


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
VALUES ('imnew', 'pass123','@jackyteojianqi'),
('logi', 'pass123','@erlynnehazey');

-- ---------------------------------------------------------------- --
--                     PAYMENT_LOG TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `PAYMENT_LOG` --
--

DROP TABLE IF EXISTS PAYMENT_LOG;
CREATE TABLE PAYMENT_LOG(
	TRANSACTIONID varchar(64) NOT NULL,
	CONSUMERID varchar(64) NOT NULL,
    CREATORID varchar(64) NOT NULL,
	PAYMENT_AMOUNT decimal(10,2) NOT NULL,
	TRANSACTION_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (TRANSACTIONID)
) ENGINE=InnoDB;


INSERT INTO PAYMENT_LOG(TRANSACTIONID,CONSUMERID,CREATORID,PAYMENT_AMOUNT) 
VALUES 
('T001', 'CON001', "CR002", "59.90")