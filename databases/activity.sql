-- Database: `activity`
--

DROP DATABASE IF EXISTS `ACTIVITY`;
CREATE DATABASE IF NOT EXISTS `ACTIVITY` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ACTIVITY`;

CREATE TABLE IF NOT EXISTS `ACTIVITY` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(64) NOT NULL,
  `log_content` varchar(500) NOT NULL,
  `log_from` varchar(128) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;