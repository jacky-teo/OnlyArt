-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 11, 2022 at 11:12 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

--
-- Database: `OnlyFence`
--
CREATE DATABASE IF NOT EXISTS ONLYFENCE DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE ONLYFENCE;

-- --------------------------------------------------------

--
-- Table structure for table `CREATORACCOUNT`
--
DROP TABLE IF EXISTS CREATORACCOUNT_SEQ;
CREATE TABLE CREATORACCOUNT_SEQ
(
  CREATORID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS CREATORACCOUNT;
CREATE TABLE IF NOT EXISTS CREATORACCOUNT (
  CREATORID varchar(64) NOT NULL,
  USERNAME varchar(64) NOT NULL,
  PASSWORD varchar(64) NOT NULL,
  EMAIL varchar(64) NOT NULL,
  PRICE decimal(10,2) NOT NULL,
  PRIMARY KEY (CREATORID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Trigger for autoincrement for `CREATORACCOUNT`
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
-- Insert Data into `CREATORACCOUNT`
--
INSERT INTO CREATORACCOUNT(USERNAME,PASSWORD,EMAIL,PRICE) 
VALUES 
('jackyteo', 'pass123', 'jacky.teo.2020@smu.edu.sg',100.00),
('notJacky', 'pass123', 'jackyteojianqi@gmail.com',233.50);
