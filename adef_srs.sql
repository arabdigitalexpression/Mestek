-- MariaDB dump 10.19  Distrib 10.5.18-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: adef_srs
-- ------------------------------------------------------
-- Server version	10.5.18-MariaDB

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
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c343137cb1a3');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar`
--

LOCK TABLES `calendar` WRITE;
/*!40000 ALTER TABLE `calendar` DISABLE KEYS */;
INSERT INTO `calendar` VALUES (1,'2022-07-19'),(2,'2023-03-19'),(3,'2023-03-21'),(4,'2022-07-27'),(5,'2022-07-29'),(8,'2023-04-13'),(9,'2023-04-15'),(10,'2023-03-12'),(11,'2023-03-13'),(12,'2023-03-14'),(13,'2023-03-15'),(14,'2023-03-16');
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
  `name` varchar(64) NOT NULL,
  `color_code` varchar(10) NOT NULL,
  `is_organization` tinyint(1) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
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
INSERT INTO `category` VALUES (1,'طالب/طلبة','#1a5fb4',0,NULL),(2,'مشروع ناشئ غير ممول','#050202',0,'فرد/فرقة محلية/ مجموعة عمل/مشروع'),(3,'مشروع ناشئ ممول','#c2a147',0,'3	فرد/فرقة محلية/ مجموعة عمل/مشروع'),(4,'مشروع او فرد ثقيل','#fed443',0,NULL),(5,'مؤسسة محلية/تجارية','#136564',1,'(فيلم تجاري، مغني او فرقة الخ)'),(6,'مؤسسة إقليمية/عربية','#34def2',1,''),(7,'مؤسسة دولية','#aeda45',1,'');
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
  `unit` enum('hour','day') DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `price_unit` enum('egp','usd') DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`space_id`,`unit`,`unit_value`),
  KEY `space_id` (`space_id`),
  CONSTRAINT `category_space_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `category_space_ibfk_2` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=415 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_space`
--

LOCK TABLES `category_space` WRITE;
/*!40000 ALTER TABLE `category_space` DISABLE KEYS */;
INSERT INTO `category_space` VALUES (233,1,6,'hour',2,'egp',646),(234,2,6,'hour',2,'egp',4566),(235,3,6,'hour',2,'egp',465),(236,4,6,'hour',2,'egp',4565),(237,5,6,'hour',2,'egp',6),(238,6,6,'hour',2,'usd',5645),(239,7,6,'hour',2,'usd',6),(240,1,6,'day',4,'egp',4564),(241,2,6,'day',4,'egp',646),(242,3,6,'day',4,'egp',456),(243,4,6,'day',4,'egp',45645),(244,5,6,'day',4,'egp',56546),(245,6,6,'day',4,'usd',20),(246,7,6,'day',4,'usd',2),(268,1,7,'hour',2,'usd',23),(269,2,7,'hour',2,'usd',40),(270,3,7,'hour',2,'egp',60),(271,4,7,'hour',2,'egp',70),(272,5,7,'hour',2,'egp',90),(273,6,7,'hour',2,'egp',5245),(274,7,7,'hour',2,'egp',70),(275,1,7,'hour',4,'usd',40),(276,2,7,'hour',4,'usd',80),(277,3,7,'hour',4,'egp',120),(278,4,7,'hour',4,'egp',241),(279,5,7,'hour',4,'egp',124213),(280,6,7,'hour',4,'egp',12421),(281,7,7,'hour',4,'egp',12312),(282,1,7,'day',1,'usd',230),(283,2,7,'day',1,'usd',230),(284,3,7,'day',1,'egp',230),(285,4,7,'day',1,'egp',230),(286,5,7,'day',1,'egp',230),(287,6,7,'day',1,'egp',230),(288,7,7,'day',1,'egp',230),(331,1,4,'day',1,'egp',254),(332,2,4,'day',1,'egp',545),(333,3,4,'day',1,'egp',58),(334,4,4,'day',1,'egp',542),(335,5,4,'day',1,'egp',45),(336,6,4,'day',1,'egp',575),(337,7,4,'day',1,'egp',75),(345,1,1,'hour',3,'egp',2424),(346,2,1,'hour',3,'egp',242),(347,3,1,'hour',3,'egp',2),(348,4,1,'hour',3,'egp',42),(349,5,1,'hour',3,'egp',242),(350,6,1,'hour',3,'egp',4242),(351,7,1,'hour',3,'egp',24),(352,1,1,'hour',6,'egp',5),(353,2,1,'hour',6,'egp',10),(354,3,1,'hour',6,'egp',15),(355,4,1,'hour',6,'egp',20),(356,5,1,'hour',6,'egp',25),(357,6,1,'hour',6,'egp',30),(358,7,1,'hour',6,'egp',35),(387,1,2,'hour',2,'egp',6),(388,2,2,'hour',2,'egp',545),(389,3,2,'hour',2,'egp',545),(390,4,2,'hour',2,'egp',455),(391,5,2,'hour',2,'egp',454),(392,6,2,'hour',2,'egp',545),(393,7,2,'hour',2,'egp',45),(394,1,2,'hour',4,'egp',20),(395,2,2,'hour',4,'egp',2),(396,3,2,'hour',4,'egp',2),(397,4,2,'hour',4,'egp',2421),(398,5,2,'hour',4,'egp',2),(399,6,2,'hour',4,'egp',12421),(400,7,2,'hour',4,'egp',12312),(401,1,2,'hour',6,'egp',51651),(402,2,2,'hour',6,'egp',16516),(403,3,2,'hour',6,'egp',6151),(404,4,2,'hour',6,'egp',420),(405,5,2,'hour',6,'egp',616516),(406,6,2,'hour',6,'egp',260),(407,7,2,'hour',6,'egp',616),(408,1,2,'day',2,'egp',20),(409,2,2,'day',2,'egp',40),(410,3,2,'day',2,'egp',60),(411,4,2,'day',2,'egp',70),(412,5,2,'day',2,'egp',90),(413,6,2,'day',2,'usd',110),(414,7,2,'day',2,'usd',110);
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
  `unit` enum('hour','day','gram','trivial') DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `price_unit` enum('egp','usd') DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`tool_id`,`unit`,`unit_value`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `category_tool_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `category_tool_ibfk_2` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_tool`
--

LOCK TABLES `category_tool` WRITE;
/*!40000 ALTER TABLE `category_tool` DISABLE KEYS */;
INSERT INTO `category_tool` VALUES (57,1,1,'day',2,'egp',50),(58,2,1,'day',2,'egp',100),(59,3,1,'day',2,'egp',120),(60,4,1,'day',2,'egp',150),(61,5,1,'day',2,'egp',210),(62,6,1,'day',2,'usd',50),(63,7,1,'day',2,'usd',90),(71,1,6,'hour',2,'egp',454),(72,2,6,'hour',2,'egp',454),(73,3,6,'hour',2,'egp',454),(74,4,6,'hour',2,'egp',452),(75,5,6,'hour',2,'egp',79),(76,6,6,'hour',2,'egp',64),(77,7,6,'hour',2,'egp',646),(78,1,2,'trivial',1,'egp',221),(79,2,2,'trivial',1,'egp',212),(80,3,2,'trivial',1,'egp',2121),(81,4,2,'trivial',1,'egp',212),(82,5,2,'trivial',1,'egp',1212),(83,6,2,'trivial',1,'egp',1221),(84,7,2,'trivial',1,'egp',22121),(85,1,3,'trivial',1,'egp',5),(86,2,3,'trivial',1,'egp',5),(87,3,3,'trivial',1,'egp',5),(88,4,3,'trivial',1,'egp',5),(89,5,3,'trivial',1,'egp',5),(90,6,3,'trivial',1,'egp',5),(91,7,3,'trivial',1,'egp',5),(92,1,4,'trivial',1,'egp',20),(93,2,4,'trivial',1,'egp',25),(94,3,4,'trivial',1,'egp',30),(95,4,4,'trivial',1,'egp',35),(96,5,4,'trivial',1,'egp',40),(97,6,4,'trivial',1,'usd',45),(98,7,4,'trivial',1,'usd',50);
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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (37,'/uploads/tool/ed246610-bb59-11ed-8a82-54271e8cb899995644_1482693008653719_6087049128942722753_n.jpg',NULL,6);
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interval`
--

LOCK TABLES `interval` WRITE;
/*!40000 ALTER TABLE `interval` DISABLE KEYS */;
INSERT INTO `interval` VALUES (1,'10:00:00','12:00:00',1,3),(2,'12:00:00','14:00:00',1,3),(3,'14:00:00','16:00:00',2,2),(4,'16:00:00','18:00:00',3,2),(5,'12:00:00','14:00:00',3,3),(6,'14:00:00','16:00:00',3,3),(13,'12:00:00','14:00:00',8,NULL),(14,'12:00:00','14:00:00',9,NULL),(15,'11:30:00','13:30:00',10,NULL),(16,'11:30:00','13:30:00',11,NULL),(17,'11:30:00','13:30:00',12,NULL),(18,'11:30:00','13:30:00',13,NULL),(19,'11:30:00','13:30:00',14,NULL);
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
  `name` varchar(64) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `address` varchar(200) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `logo_url` varchar(128) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `website_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `organization_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (1,'مدى مصر','asdas da da da ','Egypt, Cairo',6,'','23546451516','hanyasser@github.com'),(2,'أضف','مؤسسة التعبير الرقمي العربي (أضِف) ADEFمؤسسة التعبير الرقمي العربي (أضِف) ADEF ',NULL,5,'',NULL,NULL),(3,'ألوان','شيسيشسي','',6,NULL,'','');
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
  `type` enum('space','tool') NOT NULL,
  `payment_status` enum('no_payment','down_payment','full_payment') NOT NULL,
  `transaction_num` varchar(128) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `full_price` float NOT NULL,
  `space_id` int(11) DEFAULT NULL,
  `tool_id` int(11) DEFAULT NULL,
  `description` varchar(2048) NOT NULL,
  `attendance_num` int(11) DEFAULT NULL,
  `min_age` int(11) DEFAULT NULL,
  `max_age` int(11) DEFAULT NULL,
  `discount` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `space_id` (`space_id`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `reservation_ibfk_3` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`),
  CONSTRAINT `reservation_ibfk_4` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
INSERT INTO `reservation` VALUES (1,'space','no_payment','451ds-d15sd-d41s5','2022-07-12 05:24:33',2,3837,1,NULL,'',NULL,NULL,NULL,0),(2,'space','full_payment','451ds-d15sd-d41s5','2022-07-14 11:24:33',2,8338.24,2,NULL,'',NULL,NULL,NULL,0),(3,'tool','down_payment',NULL,'2022-07-15 11:24:33',1,388.85,NULL,2,'',NULL,NULL,NULL,0),(4,'space','no_payment',NULL,'2022-07-15 04:24:33',2,3873,2,NULL,'',NULL,NULL,NULL,0),(6,'space','no_payment',NULL,'2022-07-19 11:24:33',1,2028.5,1,NULL,'',NULL,NULL,NULL,0),(7,'tool','down_payment',NULL,'2022-07-21 02:24:33',2,202,NULL,3,'',NULL,NULL,NULL,0),(8,'tool','full_payment','115dw-dw15d-f5t','2022-07-30 11:24:33',1,50,NULL,1,'',NULL,NULL,NULL,0),(9,'space','no_payment',NULL,'2022-07-30 05:24:33',2,2537,1,NULL,'',NULL,NULL,NULL,0),(10,'space','down_payment',NULL,'2022-07-31 09:46:33',2,83,1,NULL,'',NULL,NULL,NULL,0),(12,'space','no_payment',NULL,'2023-03-07 23:38:20',2,1308,2,NULL,'ورشة أردوينو ',8,16,18,0),(13,'space','no_payment',NULL,'2023-03-07 23:38:20',NULL,3270,2,NULL,'sdasdasd',3,3,3,0),(14,'space','no_payment',NULL,'2023-03-08 11:38:23',NULL,0,1,NULL,'',0,0,0,0);
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation_calendar`
--

LOCK TABLES `reservation_calendar` WRITE;
/*!40000 ALTER TABLE `reservation_calendar` DISABLE KEYS */;
INSERT INTO `reservation_calendar` VALUES (3,1),(2,3),(2,2),(12,8),(12,9),(13,10),(13,11),(13,12),(13,13),(13,14);
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
INSERT INTO `reservation_tool` VALUES (1,2),(1,1),(2,1),(4,1),(1,3),(6,4),(6,1),(6,3),(12,4),(12,6),(13,4),(13,6);
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
  `name` varchar(80) NOT NULL,
  `color_code` varchar(10) NOT NULL,
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
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `guidelines` varchar(2048) NOT NULL,
  `has_operator` tinyint(1) NOT NULL,
  `capacity` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space`
--

LOCK TABLES `space` WRITE;
/*!40000 ALTER TABLE `space` DISABLE KEYS */;
INSERT INTO `space` VALUES (1,'المرقص','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، لقد تم توليد هذا النص من مولد النص العربى، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.<br>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</p><p><br>&nbsp;</p>','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، لقد تم توليد هذا النص من مولد النص العربى، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.<br>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</p><p><br>&nbsp;</p>',0,20),(2,'الرووف','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، لقد تم توليد هذا النص من مولد النص العربى، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.<br>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</p>','<ol><li>&nbsp;الالتزام بارتداء أدوات السلامة.</li><li>&nbsp;تجهيز مكان العمل بكل ما ستحتاج إليه ليكون بجوارك على منضدة العمل.</li><li>تأكد من وجود أغطية الشفرات في أماكنها ومثبتة جيداً في المعدات الكهربائية كالمناشير والصواريخ.</li><li>&nbsp;تأكد من عدم وجود أي جسم أو بقايا أخشاب قريبة من الشفرات قبل بداية تشغيلها.</li><li>استخدام توصيلات كهربائية آمنة وطويلة للحرية أثناء استخدام الأجهزة الكهربائية وتأكد من بعدها عن شفرات المعدات.</li><li>قم بمسك المعدة المخصصة للقطع أو النشر في وضعية صحيحة دون ميلان.</li><li>لا تقم بقص أو نشر القطع الخشبية الصغيرة التي تجعل أصابعك قريبة من شفرة المُعدة ولكن استخدم بدلا عن ذلك قطعة أخرى مناسبة مخصصة للضغط عليها وتحريكها بها وخاصة في المعدات والآلات الثابتة ذات الشفرات.</li><li>لا تُقرب أطرافك من شفرات المعدة أثناء عملها إطلاقاً مهما كانت الأسباب.</li><li>لا تقم بعمل أي صيانة أو تغيير لشفرات المعدة إلا بعد أن تتوقف الشفرة تماماً وتقوم بإزالة مقبس المُعدة من الكهرباء.</li><li>لا تترك المعدة بمقبس الكهرباء بعد الانتهاء من العمل.</li><li>يجب أن تكون شفرات المعدة سليمة وحادة قبل الاستخدام.</li></ol><p><i>لا تستخدم المعدات والآلات الكهربائية التي تحتوي على شفرات حادة وأنت على عجلة من أمرك، أو مشتت التركيز، أو تريد النوم، أو وأنت منشغل في شيء أخر، أو وأنت تتحدث مع أخر وتنظر له، ولا تنظر أبداً في غير موضع الشفرة وقطعة العمل أثناء عملها مهما حدث من حولك، ولا تستخدمها أبداً وهناك شيء يحجب عنك رؤية الشفرة وقطعة العمل، ويمنع استخدامها عند أخذ أية أدوية يُمنع معها القيادة</i></p>',1,25),(3,'المشغل','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، لقد تم توليد هذا النص من مولد النص العربى، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.<br>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</p><p><br>&nbsp;</p>','<p>ييشبشبشبشب</p>',0,27),(4,'معمل الحواسيب','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، <strong>لقد تم توليد هذا النص من مولد النص العربى</strong>، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.</p><p><br><i>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</i></p>','<p>هذا النص هو مثال لنص يمكن أن يستبدل في نفس المساحة، <strong>لقد تم توليد هذا النص من مولد النص العربى</strong>، حيث يمكنك أن تولد مثل هذا النص أو العديد من النصوص الأخرى إضافة إلى زيادة عدد الحروف التى يولدها التطبيق.<br>إذا كنت تحتاج إلى عدد أكبر من الفقرات يتيح لك مولد النص العربى زيادة عدد الفقرات كما تريد، النص لن يبدو مقسما ولا يحوي أخطاء لغوية، مولد النص العربى مفيد لمصممي المواقع على وجه الخصوص، حيث يحتاج العميل فى كثير من الأحيان أن يطلع على صورة حقيقية لتصميم الموقع.<br>ومن هنا وجب على المصمم أن يضع نصوصا مؤقتة على التصميم ليظهر للعميل الشكل كاملاً،دور مولد النص العربى أن يوفر على المصمم عناء البحث عن نص بديل لا علاقة له بالموضوع الذى يتحدث عنه التصميم فيظهر بشكل لا يليق.</p><p><br><i>هذا النص يمكن أن يتم تركيبه على أي تصميم دون مشكلة فلن يبدو وكأنه نص منسوخ، غير منظم، غير منسق، أو حتى غير مفهوم. لأنه مازال نصاً بديلاً ومؤقتاً.</i></p>',1,32),(6,'odoo_db','','',0,43),(7,'مساحة الإيجارات الثابتة نسبياً','<p>sadsadasdsad</p>','<p>sadsadsadasdad</p>',1,23);
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
  `name` varchar(50) NOT NULL,
  `description` varchar(2048) NOT NULL,
  `guidelines` varchar(2048) NOT NULL,
  `has_operator` tinyint(1) NOT NULL,
  `space_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `space_id` (`space_id`),
  CONSTRAINT `tool_ibfk_1` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool`
--

LOCK TABLES `tool` WRITE;
/*!40000 ALTER TABLE `tool` DISABLE KEYS */;
INSERT INTO `tool` VALUES (1,'تو تو','<p>يشسيسشيسشي سي شسي سشيسشي شس</p>','<p>يشسي سشي شي</p>',1,NULL,3),(2,'تنورة','<p>شسيسشيش سي سيشس</p>','<p>ي شسيشسيشسي</p>',0,1,5),(3,'Sony A7  ','<p>Sony A7 OR Sony A 6600</p>','<p>Sony A7 OR Sony A 6600</p>',1,1,2),(4,'كاميرا','<p>dasdasdsad</p>','<p>sadsadasdasdad</p>',1,2,6),(6,'بروجيكتور','','',0,2,3);
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
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `username` varchar(64) NOT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `role_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `phone` varchar(32) NOT NULL,
  `website_url` varchar(128) DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `activated` tinyint(1) NOT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  `gender` enum('male','female','prefer_not_answer') DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'أحمد','رمضان','ramadan','askme557@gmail.com','pbkdf2:sha256:260000$9QdxVObilSi33bK1$50d05d368af305dfabaf9b2d2397d9173c3ba5ab4b7418ab587a6644d6855a45',1,5,'2022-07-30 11:11:56','+201062894694','','','2022-12-22',1,'','male',2),(2,'يوسف','محمد','devjoe','devjoe@github.net','pbkdf2:sha256:260000$zQuiWoVfXJseAUDY$c0834e6c17ffb447ead9cba06ef8d092b6db4f1136bf40992a761ab47eef5a8f',2,6,'2022-07-30 11:11:56','+201113319016','https://www.joe.dev','Egypt, Cairo','2022-12-07',1,NULL,'male',3),(3,'محمد ','مجدى','mmagdy','magdyos@gmail.com','pbkdf2:sha256:260000$eyRXlI4NZr902feq$60e3dd712be037c7e3b7c33cbbd382b8cd6f5a70f49f1327cdf0d877525f70cf',2,1,'2022-12-11 15:23:43','01062632649','www.magdyos.com','Egypt, Cairo','2022-12-13',0,NULL,'prefer_not_answer',NULL);
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

-- Dump completed on 2023-03-28 11:45:39
