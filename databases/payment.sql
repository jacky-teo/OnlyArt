-- Database: `payment`
--
CREATE DATABASE IF NOT EXISTS PAYMENT;
USE PAYMENT;

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