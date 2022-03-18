-- Database: `notification`
--
CREATE DATABASE IF NOT EXISTS `notification` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `notification`;

-- ---------------------------------------------------------------- --
--                     NOTIFICATION TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `notification`;
CREATE TABLE IF NOT EXISTS `notification` (
  `chatid` varchar(64) NOT NULL,
  `telegramtag` varchar(64) NOT NULL,
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;