-- MariaDB dump 10.19  Distrib 10.5.16-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: adef_srs
-- ------------------------------------------------------
-- Server version	10.5.16-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('b4a2fe3f626e');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calendar`
--

DROP TABLE IF EXISTS `calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar`
--

LOCK TABLES `calendar` WRITE;
/*!40000 ALTER TABLE `calendar` DISABLE KEYS */;
INSERT INTO `calendar` VALUES (1,'2022-07-19'),(2,'2022-07-20'),(3,'2022-07-26'),(4,'2022-07-27'),(5,'2022-07-29');
/*!40000 ALTER TABLE `calendar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color_code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_organization` tinyint(1) NOT NULL,
  `description` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color_code` (`color_code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'طالب/طلبة','#1a5fb4',0,NULL),(2,'مشروع ناشئ غير ممول','#050202',0,'فرد/فرقة محلية/ مجموعة عمل/مشروع'),(3,'مشروع ناشئ ممول','#457468',0,'3	فرد/فرقة محلية/ مجموعة عمل/مشروع'),(4,'مشروع او فرد ثقيل','#fed443',0,NULL),(5,'مؤسسة محلية/تجارية','#136564',1,'(فيلم تجاري، مغني او فرقة الخ)'),(6,'مؤسسة إقليمية/عربية','#34def2',1,''),(7,'مؤسسة دولية','#aeda45',1,'');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_space`
--

DROP TABLE IF EXISTS `category_space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category_space` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `space_id` int(11) NOT NULL,
  `unit` enum('hour','day') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `price_unit` enum('egp','usd') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`space_id`,`unit`,`unit_value`),
  KEY `space_id` (`space_id`),
  CONSTRAINT `category_space_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `category_space_ibfk_2` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_space`
--

LOCK TABLES `category_space` WRITE;
/*!40000 ALTER TABLE `category_space` DISABLE KEYS */;
/*!40000 ALTER TABLE `category_space` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_tool`
--

DROP TABLE IF EXISTS `category_tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `tool_id` int(11) NOT NULL,
  `unit` enum('hour','day','gram') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `price_unit` enum('egp','usd') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`tool_id`,`unit`,`unit_value`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `category_tool_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `category_tool_ibfk_2` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_tool`
--

LOCK TABLES `category_tool` WRITE;
/*!40000 ALTER TABLE `category_tool` DISABLE KEYS */;
/*!40000 ALTER TABLE `category_tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(128) NOT NULL,
  `space_id` int(11) DEFAULT NULL,
  `tool_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `space_id` (`space_id`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`),
  CONSTRAINT `image_ibfk_2` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (10,'/uploads/tool/9cf1a322-4581-11ed-8720-54271e8cb899-cf2594f84242d332889bed5a9973a662.jpg',NULL,4),(11,'/uploads/tool/9cf24cfa-4581-11ed-8720-54271e8cb899-CpKm0YY.jpg',NULL,4),(12,'/uploads/tool/9cf280bc-4581-11ed-8720-54271e8cb899-FB_IMG_1451435871419.jpg',NULL,4),(13,'/uploads/tool/9cf2a588-4581-11ed-8720-54271e8cb899-mikasa-ackerman-attack-on-titan-28254-1920x1080.jpg',NULL,4),(14,'/uploads/tool/9cf31cc0-4581-11ed-8720-54271e8cb899-mtRHVTY.jpg',NULL,4);
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interval`
--

DROP TABLE IF EXISTS `interval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interval` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `calendar_id` int(11) DEFAULT NULL,
  `reservation_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `calendar_id` (`calendar_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `interval_ibfk_1` FOREIGN KEY (`calendar_id`) REFERENCES `calendar` (`id`) ON DELETE CASCADE,
  CONSTRAINT `interval_ibfk_2` FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interval`
--

LOCK TABLES `interval` WRITE;
/*!40000 ALTER TABLE `interval` DISABLE KEYS */;
INSERT INTO `interval` VALUES (1,'10:00:00','12:00:00',1,3),(2,'12:00:00','14:00:00',1,3),(3,'14:00:00','16:00:00',2,2),(4,'16:00:00','18:00:00',2,2),(5,'12:00:00','14:00:00',3,3),(6,'14:00:00','16:00:00',3,3);
/*!40000 ALTER TABLE `interval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `organization_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (1,'مدى مصر','مدى مصر',NULL,5),(2,'أضف','مؤسسة التعبير الرقمي العربي (أضِف) ADEFمؤسسة التعبير الرقمي العربي (أضِف) ADEF\n ',NULL,5);
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('space','tool') COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` enum('no_payment','down_payment','full_payment') COLLATE utf8mb4_unicode_ci NOT NULL,
  `transaction_num` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `full_price` float NOT NULL,
  `space_id` int(11) DEFAULT NULL,
  `tool_id` int(11) DEFAULT NULL,
  `description` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attendance_num` int(11) DEFAULT NULL,
  `min_age` int(11) DEFAULT NULL,
  `max_age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `space_id` (`space_id`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `reservation_ibfk_3` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`),
  CONSTRAINT `reservation_ibfk_4` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
INSERT INTO `reservation` VALUES (1,'space','no_payment','451ds-d15sd-d41s5','2022-07-12 05:24:33',2,3837,1,NULL,'',NULL,NULL,NULL),(2,'space','full_payment','451ds-d15sd-d41s5','2022-07-14 11:24:33',2,8338.24,1,NULL,'',NULL,NULL,NULL),(3,'tool','down_payment',NULL,'2022-07-15 11:24:33',1,388.85,NULL,2,'',NULL,NULL,NULL),(4,'space','no_payment',NULL,'2022-07-15 04:24:33',2,3873,1,NULL,'',NULL,NULL,NULL),(6,'space','no_payment',NULL,'2022-07-19 11:24:33',1,2028.5,1,NULL,'',NULL,NULL,NULL),(7,'tool','down_payment',NULL,'2022-07-21 02:24:33',2,202,NULL,3,'',NULL,NULL,NULL),(8,'tool','full_payment','115dw-dw15d-f5t','2022-07-30 11:24:33',1,50,NULL,1,'',NULL,NULL,NULL),(9,'space','no_payment',NULL,'2022-07-30 05:24:33',2,2537,1,NULL,'',NULL,NULL,NULL),(10,'space','down_payment',NULL,'2022-07-31 09:46:33',2,83,1,NULL,'',NULL,NULL,NULL);
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation_calendar`
--

DROP TABLE IF EXISTS `reservation_calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation_calendar` (
  `reservation_id` int(11) DEFAULT NULL,
  `calendar_id` int(11) DEFAULT NULL,
  KEY `calendar_id` (`calendar_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `reservation_calendar_ibfk_1` FOREIGN KEY (`calendar_id`) REFERENCES `calendar` (`id`),
  CONSTRAINT `reservation_calendar_ibfk_2` FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation_calendar`
--

LOCK TABLES `reservation_calendar` WRITE;
/*!40000 ALTER TABLE `reservation_calendar` DISABLE KEYS */;
INSERT INTO `reservation_calendar` VALUES (3,1),(3,3),(2,2);
/*!40000 ALTER TABLE `reservation_calendar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation_tool`
--

DROP TABLE IF EXISTS `reservation_tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation_tool` (
  `reservation_id` int(11) DEFAULT NULL,
  `tool_id` int(11) DEFAULT NULL,
  KEY `reservation_id` (`reservation_id`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `reservation_tool_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`id`),
  CONSTRAINT `reservation_tool_ibfk_2` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation_tool`
--

LOCK TABLES `reservation_tool` WRITE;
/*!40000 ALTER TABLE `reservation_tool` DISABLE KEYS */;
INSERT INTO `reservation_tool` VALUES (1,2),(1,1),(2,1),(4,1),(1,3),(6,4),(6,1),(6,3);
/*!40000 ALTER TABLE `reservation_tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color_code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color_code` (`color_code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin','#e01b24'),(2,'user','#2ec27e');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `space`
--

DROP TABLE IF EXISTS `space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `space` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `guidelines` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `has_operator` tinyint(1) NOT NULL,
  `capacity` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space`
--

LOCK TABLES `space` WRITE;
/*!40000 ALTER TABLE `space` DISABLE KEYS */;
INSERT INTO `space` VALUES (1,'المرقص','<p>Lmaoooo</p>','<p>Loooooool</p>',0,20),(2,'الرووف','يشيشيشبشب ','بيبشبشبشبشب',0,25),(3,'المشغل','يسيسيشسيشسي','ييشبشبشبشب',0,27),(4,'معمل الحواسيب','<p>يشبتشبىشتبىتن</p>','<p>بيىشبتشىيبشىبتسم</p>',1,32);
/*!40000 ALTER TABLE `space` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tool`
--

DROP TABLE IF EXISTS `tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guidelines` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `has_operator` tinyint(1) NOT NULL,
  `space_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `space_id` (`space_id`),
  CONSTRAINT `tool_ibfk_1` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool`
--

LOCK TABLES `tool` WRITE;
/*!40000 ALTER TABLE `tool` DISABLE KEYS */;
INSERT INTO `tool` VALUES (1,'تو تو','يشسيسشيسشي سي شسي سشيسشي شس',' يشسي سشي شي ',1,NULL,NULL),(2,'تنورة','شسيسشيش سي سيشس','ي شسيشسيشسي',0,1,NULL),(3,'Sony A7 OR Sony A 6600 ','Sony A7 OR Sony A 6600 ','Sony A7 OR Sony A 6600 ',1,NULL,NULL),(4,'كاميرا','dasdasdsad','sadsadasdasdad',1,2,NULL);
/*!40000 ALTER TABLE `tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `website_url` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `activated` tinyint(1) NOT NULL,
  `avatar_url` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` enum('male','female','prefer_not_answer') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `category_id` (`category_id`),
  KEY `role_id` (`role_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_ibfk_3` FOREIGN KEY (`organization_id`) REFERENCES `organization` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ahmed','Ramadan','ramadan','askme557@gmail.com','pbkdf2:sha256:260000$9QdxVObilSi33bK1$50d05d368af305dfabaf9b2d2397d9173c3ba5ab4b7418ab587a6644d6855a45',1,5,'2022-07-30 11:11:56','+201062894694',NULL,NULL,NULL,1,NULL,'male',2),(2,'Dev','Joe','devjoe','devjoe@github.com','pbkdf2:sha256:260000$LeoQXSvt0ZtAj1lU$38c2166ac2c4e9cdb0566c5fc6f9fa533204562c448df0391985da5bb42776b5',2,1,'2022-07-30 11:11:56','+201113319016','https://www.joe.dev',NULL,NULL,1,'https://png.pngtree.com/png-clipart/20200819/ourlarge/pngtree-female-profile-avatar-elements-png-image_2326125.jpg','male',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-04  1:35:34
