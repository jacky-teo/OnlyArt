-- Database: `notification`
--
CREATE DATABASE IF NOT EXISTS NOTIFICATION;
USE NOTIFICATION;

-- ---------------------------------------------------------------- --
--                     NOTIFICATION TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS NOTIFICATION;
CREATE TABLE NOTIFICATION(
	CHATID varchar(64) NOT NULL,
    TELEGRAMTAG varchar(64) NOT NULL,
	PRIMARY KEY (CHATID)
) ENGINE=InnoDB;