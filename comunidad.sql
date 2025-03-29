# ************************************************************
# Antares - SQL Client
# Version 0.7.34
# 
# https://antares-sql.app/
# https://github.com/antares-sql/antares
# 
# Host: 5.135.142.36 (Ubuntu 22.04 10.6.12)
# Database: comunidad
# Generation time: 2025-03-27T12:23:52+01:00
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table datadis
# ------------------------------------------------------------

DROP TABLE IF EXISTS `datadis`;

CREATE TABLE `datadis` (
  `sidn` int(11) NOT NULL,
  `cups` char(36) DEFAULT NULL,
  `cif` char(20) NOT NULL,
  `datadis_dist_code` smallint(5) unsigned DEFAULT NULL,
  `datadis_point_type` smallint(5) unsigned DEFAULT NULL,
  `energy` float DEFAULT NULL,
  `data_last` datetime DEFAULT NULL,
  PRIMARY KEY (`sidn`),
  CONSTRAINT `datadis_ibfk_1` FOREIGN KEY (`sidn`) REFERENCES `sensors` (`sidn`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;



# Dump of table e_community
# ------------------------------------------------------------

DROP TABLE IF EXISTS `e_community`;

CREATE TABLE `e_community` (
  `cidn` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(32) DEFAULT NULL,
  `pass` char(12) DEFAULT NULL,
  `cif` char(20) DEFAULT NULL,
  `emon_key` char(32) DEFAULT NULL,
  `datadis_user` char(32) DEFAULT NULL,
  `datadis_pass` char(32) DEFAULT NULL,
  PRIMARY KEY (`cidn`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;



# Dump of table sensors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sensors`;

CREATE TABLE `sensors` (
  `sidn` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(32) DEFAULT NULL,
  `type` char(12) DEFAULT NULL,
  `emon_key` char(32) DEFAULT NULL,
  `gen_id` smallint(5) unsigned DEFAULT NULL,
  `coef` float unsigned DEFAULT NULL,
  `feed_con` int(11) DEFAULT NULL,
  `feed_gen` int(11) DEFAULT NULL,
  `autoconsumed` float DEFAULT NULL,
  `exported` float DEFAULT NULL,
  `imported` float DEFAULT NULL,
  `sen_last` datetime DEFAULT NULL,
  PRIMARY KEY (`sidn`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;



# Dump of table suministros
# ------------------------------------------------------------

DROP TABLE IF EXISTS `suministros`;

CREATE TABLE `suministros` (
  `ridn` int(11) NOT NULL AUTO_INCREMENT,
  `cif` char(20) DEFAULT NULL,
  `datadis_dist_code` int(4) NOT NULL DEFAULT 8,
  PRIMARY KEY (`ridn`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;



# Dump of views
# ------------------------------------------------------------

# Creating temporary tables to overcome VIEW dependency errors


/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

# Dump completed on 2025-03-27T12:23:52+01:00
