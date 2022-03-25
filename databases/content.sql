-- Database: `content`
--
CREATE DATABASE IF NOT EXISTS content;
USE content;

-- ---------------------------------------------------------------- --
--                     CONTENT DATABASE                        --
-- ---------------------------------------------------------------- --

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
	PRIMARY KEY (POSTID)
) ENGINE=InnoDB;


INSERT INTO CONTENT(POSTID,CREATORID,DESCRIPTION,IMAGE_ID) 
VALUES 
('CR001_IMG1','CR001', 'this is img1', "img1",'png'),
('CR001_IMG2','CR001', 'this is img2', "img2",'png'),
('CR001_IMG3','CR001', 'this is img3', "img3",'png'),
('CR001_IMG4','CR001', 'this is img4', "img4",'png'),
-- ('CR002_IMG1','CR002', 'this is cr2img1', 'cr2img1'),
-- ('CR002_IMG2','CR002', 'this is cr2img2', 'cr2img2'),
-- ('CR002_IMG3','CR002', 'this is cr2img3', 'cr2img3');