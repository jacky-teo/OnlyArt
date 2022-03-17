-- Database: `content`
--
CREATE DATABASE IF NOT EXISTS content;
USE content;

-- ---------------------------------------------------------------- --
--                     CREATOR_CONTENT TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CREATOR_CONTENT_SEQ` --
--
DROP TABLE IF EXISTS CONTENT_SEQ;
CREATE TABLE CONTENT_SEQ
(
	POSTID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CREATOR_CONTENT` --
--

DROP TABLE IF EXISTS CONTENT;
CREATE TABLE CONTENT(
	POSTID varchar(64) NOT NULL,
	CREATORID varchar(64) NOT NULL,
	DESCRIPTION varchar(64) NOT NULL,
	IMAGE_ID varchar(64) NOT NULL,
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
BEFORE INSERT ON CONTENT
FOR EACH ROW
BEGIN
	INSERT INTO CONTENT_SEQ VALUES (NULL);
	SET NEW.POSTID = CONCAT('P', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

INSERT INTO CONTENT(CREATORID,DESCRIPTION,IMAGE_ID) 
VALUES 
('CR001', 'this is img1', "img1"),
('CR001', 'this is img2', "img2"),
('CR001', 'this is img3', "img3"),
('CR001', 'this is img4', "img4"),
('CR002', 'this is cr2img1', 'cr2img1'),
('CR002', 'this is cr2img2', 'cr2img2'),
('CR002', 'this is cr2img3', 'cr2img3');