-- Database: `content`
--
CREATE DATABASE IF NOT EXISTS content;
USE content;

-- ---------------------------------------------------------------- --
--                     CONTENT DATABASE                        --
-- ---------------------------------------------------------------- --

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

--
-- Table structure for table `CONTENT` --
--

DROP TABLE IF EXISTS CONTENT;
CREATE TABLE CONTENT(
	POSTID varchar(64) NOT NULL,
	CREATORID varchar(64) NOT NULL,
	DESCRIPTION varchar(64) NOT NULL,
	IMAGE_ID varchar(64) NOT NULL,
    IMG_EXT varchar(64) NOT NULL,
	POST_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (POSTID),
	CONSTRAINT FK_CREATORID FOREIGN KEY (CREATORID) REFERENCES CREATORACCOUNT(CREATORID)
) ENGINE=InnoDB;


-- INSERT INTO CONTENT(POSTID,CREATORID,DESCRIPTION,IMAGE_ID) 
-- VALUES 
-- ('CR001_IMG1','CR001', 'this is img1', "img1"),
-- ('CR001_IMG2','CR001', 'this is img2', "img2"),
-- ('CR001_IMG3','CR001', 'this is img3', "img3"),
-- ('CR001_IMG4','CR001', 'this is img4', "img4"),
-- ('CR002_IMG1','CR002', 'this is cr2img1', 'cr2img1'),
-- ('CR002_IMG2','CR002', 'this is cr2img2', 'cr2img2'),
-- ('CR002_IMG3','CR002', 'this is cr2img3', 'cr2img3');