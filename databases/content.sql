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
('CR001_img1','CR001', 'My Hero Academia Artwork ', "img1",'jpeg'),
('CR001_img2','CR001', 'Painted a girl biting her nails', "img2",'jpeg'),
('CR001_img3','CR001', 'Red Scarf', "img3",'jpeg'),
('CR001_img4','CR001', 'Pastel painting of a girl', "img4",'jpeg'),
('CR001_img5','CR001', 'Sword Art Online', "img5",'jpeg'),
('CR001_img6','CR001', 'Blade works', "img6",'jpeg'),
('CR001_img7','CR001', 'Blue Lightning', "img7",'jpeg'),
('CR001_img8','CR001', 'Son Goku and Moon', "img8",'jpeg'),
('CR001_img9','CR001', 'WindowBlower', "img9",'jpeg'),
('CR001_img10','CR001', 'Koi fish my dreams', "img10",'jpeg'),
('CR002_img1','CR001', 'Cinna at peace', "img1",'jpeg'),
('CR002_img2','CR001', 'Cinna love', "img2",'jpeg'),
('CR002_img3','CR001', 'Cinna Relax', "img3",'jpeg'),
('CR002_img4','CR001', 'Cinna sad', "img4",'jpeg'),
('CR002_img5','CR001', 'TOO CUTE LA', "img5",'jpeg'),
('CR002_img6','CR001', 'The cutest', "img6",'jpeg'),
('CR002_img7','CR001', "I'm a detective", "img7",'jpeg'),
('CR002_img8','CR001', "I gave up on life", "img8",'jpeg'),
('CR002_img9','CR001', 'Kuromi UwU OwO', "img9",'jpeg'),
('CR002_img10','CR001', 'Melody UwU Owo', "img10",'jpeg')
