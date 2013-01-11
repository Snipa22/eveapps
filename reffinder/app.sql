-- MySQL dump 10.13  Distrib 5.5.28, for Linux (i686)
--
-- Host: localhost    Database: app
-- ------------------------------------------------------
-- Server version	5.5.28-29.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `monitor`
--

DROP TABLE IF EXISTS `monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitor` (
  `key` varchar(48) NOT NULL,
  `new` bigint(20) NOT NULL DEFAULT '0',
  `old` bigint(20) NOT NULL DEFAULT '0',
  `null` bigint(20) NOT NULL DEFAULT '0',
  `generator` varchar(256) NOT NULL DEFAULT 'Unknown',
  `total` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`key`),
  UNIQUE KEY `key_UNIQUE` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prices`
--

DROP TABLE IF EXISTS `prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prices` (
  `region` int(11) NOT NULL,
  `itemid` int(11) NOT NULL,
  `buymean` float DEFAULT '0',
  `buyavg` float DEFAULT '0',
  `sellmean` float DEFAULT '0',
  `sellavg` float DEFAULT '0',
  `buycount` float DEFAULT '0',
  `sellcount` float DEFAULT '0',
  `buy` float DEFAULT '0',
  `sell` float DEFAULT '0',
  `uniquek` varchar(45) NOT NULL,
  `dateTime` int(16) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uniquek`),
  KEY `itemid_index` (`itemid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repromin`
--

DROP TABLE IF EXISTS `repromin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repromin` (
  `typeID` int(11) NOT NULL,
  `volume` float DEFAULT NULL,
  `rate` float DEFAULT NULL,
  `Tritanium` int(11) DEFAULT NULL,
  `Pyerite` int(11) DEFAULT NULL,
  `Mexallon` int(11) DEFAULT NULL,
  `Isogen` int(11) DEFAULT NULL,
  `Nocxium` int(11) DEFAULT NULL,
  `Zydrine` int(11) DEFAULT NULL,
  `Megacyte` int(11) DEFAULT NULL,
  `Morphite` int(11) DEFAULT NULL,
  `portion` int(11) DEFAULT NULL,
  PRIMARY KEY (`typeID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-01-10 18:14:34
