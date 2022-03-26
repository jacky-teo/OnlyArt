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


INSERT INTO CONTENT(POSTID,CREATORID,DESCRIPTION,IMAGE_ID,IMG_EXT) 
VALUES 
('CR001_IMG11','CR001', 'this is img1', "img11",'png'),
('CR001_IMG12','CR001', 'this is img2', "img12",'png'),
('CR001_IMG13','CR001', 'this is img3', "img13",'png'),
('CR001_IMG14','CR001', 'this is img4', "img14",'png')
-- ('CR002_IMG1','CR002', 'this is cr2img1', 'cr2img1'),
-- ('CR002_IMG2','CR002', 'this is cr2img2', 'cr2img2'),
-- ('CR002_IMG3','CR002', 'this is cr2img3', 'cr2img3');