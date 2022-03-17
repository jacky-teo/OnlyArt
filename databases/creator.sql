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
    PAYPALID varchar(64) NOT NULL,
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
--                     CREATOR_CONTENT TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CREATOR_CONTENT_SEQ` --
--
DROP TABLE IF EXISTS CREATOR_CONTENT_SEQ;
CREATE TABLE CREATOR_CONTENT_SEQ
(
	POSTID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CREATOR_CONTENT` --
--

DROP TABLE IF EXISTS CREATOR_CONTENT;
CREATE TABLE CREATOR_CONTENT(
	POSTID varchar(64) NOT NULL,
	CREATORID varchar(64) NOT NULL,
	DESCRIPTION varchar(64) NOT NULL,
	IMAGE_URL varchar(64) NOT NULL,
	POST_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (POSTID, CREATORID),
	CONSTRAINT FK_CREATORID FOREIGN KEY (CREATORID) REFERENCES CREATORACCOUNT(CREATORID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATOR_CONTENT`
--

DELIMITER $$
CREATE TRIGGER tg_creator_content_insert
BEFORE INSERT ON CREATOR_CONTENT
FOR EACH ROW
BEGIN
	INSERT INTO CREATOR_CONTENT_SEQ VALUES (NULL);
	SET NEW.POSTID = CONCAT('P', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

INSERT INTO CREATOR_CONTENT(CREATORID,DESCRIPTION,IMAGE_URL) 
VALUES 
('CR001', 'not me', "./static/images/CR001/cr001_1.jpg"),
('CR001', 'not me', "./static/images/CR001/cr001_2.png"),
('CR002', 'please work', './static/images/CR002/cr002_1.png');
