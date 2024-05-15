-- MariaDB dump 10.19  Distrib 10.5.23-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: adef_srs
-- ------------------------------------------------------
-- Server version	10.5.23-MariaDB

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
INSERT INTO `alembic_version` VALUES ('af0764db79b5');
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar`
--

LOCK TABLES `calendar` WRITE;
/*!40000 ALTER TABLE `calendar` DISABLE KEYS */;
INSERT INTO `calendar` VALUES (1,'2022-07-19'),(2,'2023-03-19'),(3,'2023-03-21'),(4,'2022-07-27'),(5,'2022-07-29'),(8,'2023-04-13'),(9,'2023-04-15'),(10,'2023-03-12'),(11,'2023-03-13'),(12,'2023-03-14'),(13,'2023-03-15'),(14,'2023-03-16'),(22,'2023-05-08'),(23,'2023-05-09'),(24,'2023-05-09'),(25,'2023-05-13'),(26,'2023-05-14'),(27,'2023-05-15'),(28,'2023-06-02'),(29,'2023-06-08'),(30,'2023-06-07'),(31,'2023-06-06'),(32,'2023-06-05'),(33,'2023-06-04'),(34,'2023-06-03'),(35,'2023-05-30'),(36,'2023-05-31'),(37,'2023-06-14'),(38,'2023-05-31'),(39,'2024-02-26'),(40,'2024-02-27'),(41,'2024-04-16'),(42,'2024-04-17'),(43,'2024-04-16'),(44,'2024-04-17'),(45,'2024-04-16'),(46,'2024-04-17'),(47,'2024-04-16'),(48,'2024-04-17'),(49,'2024-04-21'),(50,'2024-04-22');
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
INSERT INTO `category` VALUES (1,'طالب/طلبة','#1a5fb4',0,NULL),(2,'فرد/فرقة محلية/ مجموعة عمل/مشروع ناشئ غير ممول','#050202',0,'فرد/فرقة محلية/ مجموعة عمل/مشروع'),(3,'فرد/فرقة محلية/ مجموعة عمل/مشروع ناشئ  ممول','#c2a147',0,'3	فرد/فرقة محلية/ مجموعة عمل/مشروع'),(4,'مؤسسه محلية تجارية ناشئة  (فيلم تجاري، مغني الخ)','#fed443',0,''),(5,'مؤسسة محلية تجارية راسخة (فيلم تجاري، مغني الخ)','#136564',1,'(فيلم تجاري، مغني او فرقة الخ)'),(6,'مؤسسة إقليمية/عربية','#34def2',1,''),(7,'مؤسسة دولية','#aeda45',1,'');
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
  `unit` enum('hour','day','minute') DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `price_unit` enum('egp','usd') DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`space_id`,`unit`,`unit_value`),
  KEY `space_id` (`space_id`),
  CONSTRAINT `category_space_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `category_space_ibfk_2` FOREIGN KEY (`space_id`) REFERENCES `space` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=967 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_space`
--

LOCK TABLES `category_space` WRITE;
/*!40000 ALTER TABLE `category_space` DISABLE KEYS */;
INSERT INTO `category_space` VALUES (694,1,3,'hour',1,'egp',250),(695,2,3,'hour',1,'egp',375),(696,3,3,'hour',1,'egp',500),(697,4,3,'hour',1,'egp',750),(698,5,3,'hour',1,'egp',1500),(699,6,3,'hour',1,'usd',58),(700,7,3,'hour',1,'usd',117),(701,1,3,'hour',8,'egp',1500),(702,2,3,'hour',8,'egp',2438),(703,3,3,'hour',8,'egp',3250),(704,4,3,'hour',8,'egp',4875),(705,5,3,'hour',8,'egp',9750),(706,6,3,'hour',8,'usd',379),(707,7,3,'hour',8,'usd',758),(736,1,1,'hour',1,'egp',200),(737,2,1,'hour',1,'egp',300),(738,3,1,'hour',1,'egp',400),(739,4,1,'hour',1,'egp',600),(740,5,1,'hour',1,'egp',1200),(741,6,1,'hour',1,'usd',47),(742,7,1,'hour',1,'usd',93),(743,1,1,'hour',8,'egp',1200),(744,2,1,'hour',8,'egp',1950),(745,3,1,'hour',8,'egp',2600),(746,4,1,'hour',8,'egp',3900),(747,5,1,'hour',8,'egp',7800),(748,6,1,'hour',8,'usd',303),(749,7,1,'hour',8,'usd',607),(750,1,4,'hour',1,'egp',150),(751,2,4,'hour',1,'egp',200),(752,3,4,'hour',1,'egp',200),(753,4,4,'hour',1,'egp',250),(754,5,4,'hour',1,'egp',300),(755,6,4,'hour',1,'usd',5),(756,7,4,'hour',1,'usd',10),(883,1,9,'hour',1,'egp',350),(884,2,9,'hour',1,'egp',525),(885,3,9,'hour',1,'egp',700),(886,4,9,'hour',1,'egp',1050),(887,5,9,'hour',1,'egp',2100),(888,6,9,'hour',1,'usd',82),(889,7,9,'hour',1,'usd',163),(890,1,9,'hour',8,'egp',2100),(891,2,9,'hour',8,'egp',3413),(892,3,9,'hour',8,'egp',4550),(893,4,9,'hour',8,'egp',6825),(894,5,9,'hour',8,'egp',13650),(895,6,9,'hour',8,'usd',531),(896,7,9,'hour',8,'usd',1062),(897,1,12,'hour',1,'egp',350),(898,2,12,'hour',1,'egp',525),(899,3,12,'hour',1,'egp',700),(900,4,12,'hour',1,'egp',1050),(901,5,12,'hour',1,'egp',2100),(902,6,12,'hour',1,'usd',82),(903,7,12,'hour',1,'usd',163),(904,1,12,'hour',8,'egp',2100),(905,2,12,'hour',8,'egp',3413),(906,3,12,'hour',8,'egp',4550),(907,4,12,'hour',8,'egp',6825),(908,5,12,'hour',8,'egp',13650),(909,6,12,'hour',8,'usd',531),(910,7,12,'hour',8,'usd',1062),(925,1,14,'hour',1,'egp',200),(926,2,14,'hour',1,'egp',300),(927,3,14,'hour',1,'egp',400),(928,4,14,'hour',1,'egp',600),(929,5,14,'hour',1,'egp',1200),(930,6,14,'hour',1,'usd',47),(931,7,14,'hour',1,'usd',93),(932,1,14,'hour',8,'egp',1200),(933,2,14,'hour',8,'egp',1950),(934,3,14,'hour',8,'egp',2600),(935,4,14,'hour',8,'egp',3900),(936,5,14,'hour',8,'egp',7800),(937,6,14,'hour',8,'usd',303),(938,7,14,'hour',8,'usd',607),(939,1,6,'hour',1,'egp',325),(940,2,6,'hour',1,'egp',487.5),(941,3,6,'hour',1,'egp',650),(942,4,6,'hour',1,'egp',975),(943,5,6,'hour',1,'egp',1950),(944,6,6,'hour',1,'usd',76),(945,7,6,'hour',1,'usd',152),(946,1,2,'hour',1,'egp',200),(947,2,2,'hour',1,'egp',300),(948,3,2,'hour',1,'egp',400),(949,4,2,'hour',1,'egp',600),(950,5,2,'hour',1,'egp',1200),(951,6,2,'hour',1,'usd',47),(952,7,2,'hour',1,'usd',93),(953,1,2,'hour',8,'egp',1200),(954,2,2,'hour',8,'egp',1950),(955,3,2,'hour',8,'egp',2600),(956,4,2,'hour',8,'egp',3900),(957,5,2,'hour',8,'egp',7800),(958,6,2,'hour',8,'usd',303),(959,7,2,'hour',8,'usd',607),(960,1,13,'minute',1,'egp',5),(961,2,13,'minute',1,'egp',5),(962,3,13,'minute',1,'egp',5),(963,4,13,'minute',1,'egp',5),(964,5,13,'minute',1,'egp',5),(965,6,13,'minute',1,'usd',0.5),(966,7,13,'minute',1,'usd',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_tool`
--

LOCK TABLES `category_tool` WRITE;
/*!40000 ALTER TABLE `category_tool` DISABLE KEYS */;
INSERT INTO `category_tool` VALUES (169,1,6,'trivial',1,'egp',260),(170,2,6,'trivial',1,'egp',390),(171,3,6,'trivial',1,'egp',520),(172,4,6,'trivial',1,'egp',780),(173,5,6,'trivial',1,'egp',1560),(174,6,6,'trivial',1,'usd',61),(175,7,6,'trivial',1,'usd',121),(176,1,12,'trivial',1,'egp',150),(177,2,12,'trivial',1,'egp',225),(178,3,12,'trivial',1,'egp',300),(179,4,12,'trivial',1,'egp',450),(180,5,12,'trivial',1,'egp',900),(181,6,12,'trivial',1,'usd',35),(182,7,12,'trivial',1,'usd',70);
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (38,'https://mestek.adef.xyz/uploads/space/d1c8349ac9e64a89af00464b46286ca7_ADF06031.webp',1,NULL),(39,'https://mestek.adef.xyz/uploads/space/86a8efa9eebc4e86bd2a0d6034fdd491_ADF00014.webp',12,NULL),(45,'https://mestek.adef.xyz/uploads/space/6a8d153d9fc24e43b4d0f78c79c6c792_ADF09355.webp',2,NULL),(47,'https://mestek.adef.xyz/uploads/space/6e1cca1dfb184d99a4af9c7382fef8fe_WhatsApp_Image_2024-04-0.jpeg',3,NULL),(48,'https://mestek.adef.xyz/uploads/space/d880b57773da45f88cad144db4f86019_WhatsApp_Image_2024-04-08.jpeg',3,NULL),(49,'https://mestek.adef.xyz/uploads/space/cb7402fef54147548ae0e977b3c3ad8e_WhatsApp_Image_2024-04-08_at.jpeg',3,NULL),(50,'https://mestek.adef.xyz/uploads/space/77ab7ca73895483d800865fa610e12bf_WhatsApp_Image_2024-04-08_at_2.18.26_PM.jpeg',3,NULL),(51,'https://mestek.adef.xyz/uploads/space/41d9b6d4f93d475e82a041c5829626bb_WhatsApp_Image_2024-04-08_at_2.18.27_PM.jpeg',3,NULL),(52,'https://mestek.adef.xyz/uploads/space/2ac241c7ba19400f988d2c62d486f375_WhatsApp_Image_2024-04-08_at_2PM.jpeg',3,NULL),(53,'https://mestek.adef.xyz/uploads/space/63b1cd933c664ba2974224d28cefa2be_ADF09309.webp',2,NULL),(54,'https://mestek.adef.xyz/uploads/space/0e66e50c477f438ebc102b2f765ede7b_G0023632.webp',4,NULL),(55,'https://mestek.adef.xyz/uploads/space/0fa02bbe9ea743409be7e5b2ea9337e3_Studio_Adef.jpg',6,NULL),(56,'https://mestek.adef.xyz/uploads/space/b5cb780453c04f92b1b761a7893b01dc_lcs.webp',12,NULL),(57,'https://mestek.adef.xyz/uploads/space/08730d2f813940cc976300c07a868a43_IMG_4185.webp',13,NULL),(58,'https://mestek.adef.xyz/uploads/space/6161f58b748041dbaa3af3ae7270c213_IMG_4187.webp',13,NULL),(59,'https://mestek.adef.xyz/uploads/space/de02c7a5b7114676b296a73cdfcdc366_IMG_4183.webp',9,NULL),(60,'https://mestek.adef.xyz/uploads/space/2ed980be1d31462cb7f0fe734b96b382_IMG_4184.webp',9,NULL),(61,'https://mestek.adef.xyz/uploads/space/c9508a98dec74cc9a30d41153e4ff285_2DF03256.webp',9,NULL),(62,'https://mestek.adef.xyz/uploads/space/30f5996654ec4e9dbf996791dfde7f3d_IMG_4188.webp',12,NULL),(63,'https://mestek.adef.xyz/uploads/space/868b402d369745729440ff25cf3dfd17_ADF09448.webp',14,NULL),(64,'https://mestek.adef.xyz/uploads/space/6a29ef876e164a42a12a8e0ba8e48d6b_1.jpg',6,NULL),(65,'https://mestek.adef.xyz/uploads/space/8f6ea5b1caa84fa0ab049cdfb6d23dd6_3.jpg',6,NULL),(66,'https://mestek.adef.xyz/uploads/space/839cfdc29d1d46caadc20fe42dba94e3_post-sound-studio.jpg',6,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interval`
--

LOCK TABLES `interval` WRITE;
/*!40000 ALTER TABLE `interval` DISABLE KEYS */;
INSERT INTO `interval` VALUES (13,'12:00:00','14:00:00',8,NULL),(14,'12:00:00','14:00:00',9,NULL),(15,'11:30:00','13:30:00',10,NULL),(16,'11:30:00','13:30:00',11,NULL),(17,'11:30:00','13:30:00',12,NULL),(18,'11:30:00','13:30:00',13,NULL),(19,'11:30:00','13:30:00',14,NULL),(73,'10:00:00','18:00:00',49,36),(74,'10:00:00','18:00:00',50,37);
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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
INSERT INTO `reservation` VALUES (36,'space','no_payment',NULL,'2024-04-15 08:55:26',27,1950,1,NULL,'',4,10,15,0),(37,'space','no_payment',NULL,'2024-04-15 08:55:26',27,2340,1,NULL,'dsadsa',5,5,10,0);
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
INSERT INTO `reservation_calendar` VALUES (36,49),(37,50);
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
INSERT INTO `reservation_tool` VALUES (37,6);
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
  `type` enum('undefined','coworking','residency','workshop_studio','performance_space') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space`
--

LOCK TABLES `space` WRITE;
/*!40000 ALTER TABLE `space` DISABLE KEYS */;
INSERT INTO `space` VALUES (1,'استوديو الرقص','<p>مساحة بأرضيات خشبية وجدران عاكسة مجهزة لورش رقص ومسرح ومعارض وعروض تقديمية<br>يمكن توفير بروجيكتور و سماعات برسوم منفصلة</p>','<p>الالتزام بالحضور في الموعد المحجوز.<br>2- غلق التكييف بعد استخدام المساحة.<br>3- لا يسمح بتواجد مشروبات أو المأكولات<br>داخل الاستوديو بجانب الأجهزة.<br>4 رجاء تنظيف المكان بعد الانتهاء.<br>5- يرجى الاعتناء جيدًا بالمعدات الموسيقية</p>',0,20,'performance_space'),(2,'الرووف','<p>غرفة خشب واجهات زجاج يمكن استخدامها لعمل ورش ، اجتماعات او جلسات&nbsp; يسع 10 أفراد بحد أقصى</p>','',0,10,'coworking'),(3,'المشغل','<p>مساحة عمل تشمل أدوات الفنون البصرية و اليدوية من فرش ،مقصات ، كاتر ، تربيزات عمل ، اوراق و الوان&nbsp;</p><p>بالإضافة إلى معمل نسيج يشمل 3 ماكينات خياطة و تربيزاه عمل باستخدام القماش.</p><p>المعدات:</p><ul><li>عدة نحت طين*</li><li>عدة عمل للجلود*</li><li>عدة خياطة يدوية</li><li>عدة airbrush بالوان</li><li>2 * طابع ثلاثي الابعاد fdm</li><li>طابع ثلاثي الابعاد resin</li><li>مساحة عمل للدهان والصنفرة</li></ul><p>يمكن لأكثر من فرد استخدامها في نفس الوقت بشكل فردي (مشغل الفنون&nbsp; أو&nbsp; النسيج)،&nbsp;</p><p>في حالة المجموعات أو الورش ينصح بأستخدام&nbsp; المساحه كامله (مشغل الفنون و النسيج معا)</p>','',0,10,'workshop_studio'),(4,'معمل الحاسوب','<p>معمل كمبيوتر للأغراض العامة لأي ورش عمل رقمية. مزود بـ8 أجهزة كمبيوتر وجهاز عرض و يمكن تجهيزه بأي أدوات أخرى حسب احتياجات الورشة</p>','',0,9,'workshop_studio'),(6,'استوديو صوت دكة ','<p>ستوديو الصوت في أضف للتسجيل الاحترافي وإنتاج الموسيقى والمزج وتحرير الصوت.</p><p>String Instruments:<br>Electric Guitar (Schecter diamond series 24 Frets)<br>Bass Guitar (Greg Bennet Cobra (warlock shape)<br>Oud&nbsp;<br>Classic guitar<br>Violin<br>M1 Macbook With Ableton Live 11 with a large collection of premium Vst plugins.<br>Arturia Midi Keyboard (61 Keys)<br>Yamaha Hs5 Monitor (pair)<br>Focusrite Scarlett 18i20 Soundcard (Audio Interface)<br>Xone:92 Allen &amp; Heath DJ Mixer (one day notice)<br>Active stereo Di box&nbsp;<br>8-channel Headphone Amplifier<br>Ultra Gain Pro-8 Digital 8 channel AD &amp; DA converter Model ADA800<br>Pro Fx 16 Channel<br>Headphones Sennheiser HD 206</p><p>Mics:<br>Rode NT1-A Microphone&nbsp;<br>Rode M5 Microphone&nbsp;<br>Sure SM57 Microphone&nbsp;<br>Sure SM58 Microphone<br>Sure SM27 Microphone<br>AKG C 2000 B Microphone</p>','',0,5,'workshop_studio'),(9,'المهكر الثقيل','<p>مساحة للعمل و التجريب في مجالات التصنيع التقليدي والرقمي حيث انه&nbsp; مجهز بمعدات ثقيلة لاستخدامها في الصناعات ( الخشب -اللحام..الخ)</p><p>المعدات المهكر :</p><ul><li>عدة النجارة</li><li>عدة الحدادة</li><li>مساحة عمل القوالب</li><li>مساحة عمل مفتوحة</li></ul>','<ol><li>&nbsp;الالتزام بارتداء أدوات السلامة.</li><li>&nbsp;تجهيز مكان العمل بكل ما ستحتاج إليه ليكون بجوارك على منضدة العمل.</li><li>تأكد من وجود أغطية الشفرات في أماكنها ومثبتة جيداً في المعدات الكهربائية كالمناشير والصواريخ.</li><li>&nbsp;تأكد من عدم وجود أي جسم أو بقايا أخشاب قريبة من الشفرات قبل بداية تشغيلها.</li><li>استخدام توصيلات كهربائية آمنة وطويلة للحرية أثناء استخدام الأجهزة الكهربائية وتأكد من بعدها عن شفرات المعدات.</li><li>قم بمسك المعدة المخصصة للقطع أو النشر في وضعية صحيحة دون ميلان.</li><li>لا تقم بقص أو نشر القطع الخشبية الصغيرة التي تجعل أصابعك قريبة من شفرة المُعدة ولكن استخدم بدلا عن ذلك قطعة أخرى مناسبة مخصصة للضغط عليها وتحريكها بها وخاصة في المعدات والآلات الثابتة ذات الشفرات.</li><li>لا تُقرب أطرافك من شفرات المعدة أثناء عملها إطلاقاً مهما كانت الأسباب.</li><li>لا تقم بعمل أي صيانة أو تغيير لشفرات المعدة إلا بعد أن تتوقف الشفرة تماماً وتقوم بإزالة مقبس المُعدة من الكهرباء.</li><li>لا تترك المعدة بمقبس الكهرباء بعد الانتهاء من العمل.</li><li>يجب أن تكون شفرات المعدة سليمة وحادة قبل الاستخدام.</li></ol><p><i>لا تستخدم المعدات والآلات الكهربائية التي تحتوي على شفرات حادة وأنت على عجلة من أمرك، أو مشتت التركيز، أو تريد النوم، أو وأنت منشغل في شيء أخر، أو وأنت تتحدث مع أخر وتنظر له، ولا تنظر أبداً في غير موضع الشفرة وقطعة العمل أثناء عملها مهما حدث من حولك، ولا تستخدمها أبداً وهناك شيء يحجب عنك رؤية الشفرة وقطعة العمل، ويمنع استخدامها عند أخذ أية أدوية يُمنع معها القيادة</i></p>',1,6,'workshop_studio'),(12,'المهكر الإلكتروني','<p>مساحة للعمل و التجريب في مجالات الالكترونيات.<br>المعدات:&nbsp;</p><ul><li>لوحات تطوير (Arduino - Raspberry Pi - IoT board)</li><li>مكونات إلكترونية</li><li>ادوات (Power Supply 2 channels - Function generator)</li><li>3d printers&nbsp;</li></ul>','',1,6,'workshop_studio'),(13,'معمل التصنيع الرقمي - ماكينة تقطيع كاربون ليزر','<p>ماكينة تقطيع كاربون ليزر مساحتها 160*100سم<br>&nbsp;</p>','',1,8,'workshop_studio'),(14,'مساحة مجتمعية - الدور الأرضي','<p>مساحة مجتمعية موجودة في الدور الأرضي<br><strong>مع حجز القاعه ممكن توفير كوفي كورنر حسب الطلب</strong></p>','',0,10,'coworking');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool`
--

LOCK TABLES `tool` WRITE;
/*!40000 ALTER TABLE `tool` DISABLE KEYS */;
INSERT INTO `tool` VALUES (6,'بروجيكتور استوديو الرقص','','',0,1,1),(12,'سماعات سبيكر استوديو الرقص','','',0,1,1);
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
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `category_id` (`category_id`),
  KEY `role_id` (`role_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_ibfk_3` FOREIGN KEY (`organization_id`) REFERENCES `organization` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'أحمد','رمضان','ramadan','askme557s@gmail.com','pbkdf2:sha256:260000$9QdxVObilSi33bK1$50d05d368af305dfabaf9b2d2397d9173c3ba5ab4b7418ab587a6644d6855a45',1,5,'2022-07-30 11:11:56','+201062894694','','','2022-12-22',1,'','male',2,NULL),(2,'يوسف','محمد','devjoe','devjoe@github.net','pbkdf2:sha256:260000$zQuiWoVfXJseAUDY$c0834e6c17ffb447ead9cba06ef8d092b6db4f1136bf40992a761ab47eef5a8f',2,6,'2022-07-30 11:11:56','+201113319016','https://www.joe.dev','Egypt, Cairo','2022-12-07',1,NULL,'male',3,NULL),(12,'Islam','Shabana','islam','i.shabana@arabdigitalexpression.org','pbkdf2:sha256:260000$Y3hPvLb5z5ztnMfZ$751e959b9c0c08d58b1b44ed0b26d8d8a27c2d25c7f2eb530ae49da650c170fc',1,6,'2023-05-07 23:08:04','01141962411','','','1970-01-01',1,NULL,'male',1,NULL),(16,'أحمد','مكاوى','مكاوى','mekkawy@arabdigitalexpression.org','pbkdf2:sha256:260000$qaOEgD96lsZ3xfyX$a0adbdc21520cfa090c5de2edd7124bcbcb565145698b8fd8ce2938a9771789e',1,4,'2024-01-17 12:24:16','01119999756','','','1990-10-10',1,NULL,'male',NULL,NULL),(17,'Maha','Ghaleb','Mahaabusaa','maha@arabdigitalexpression.org','pbkdf2:sha256:260000$M5bQqMqr0gswHkqX$1c611525377088aead7b6d666a158b6aac0ff21c87618249e9a769925a4d18d4',1,4,'2024-01-17 12:24:15','01117177770','','','1990-10-10',1,NULL,'female',NULL,NULL),(19,'Maha','Ghaleb','Maha2024','mahaabusaa@gmail.com','pbkdf2:sha256:260000$LgXqFQiA5Md9wQOX$7fd4dc3c6aed80c7115bd40f2faa600f57770383f7c07085ee836eb557c369fa',2,4,'2024-01-17 12:24:16','01117177770','','','1973-04-11',1,NULL,'female',NULL,NULL),(20,'نادية ','منير','نادية ','nadiamounier@arabdigitalexpression.org','pbkdf2:sha256:260000$khVypTnGRZmK5h0j$7e1cd3cf71e5381e09f66109f80430de2693f5ace7ed5798d3137b9f1e7a7905',2,2,'2024-03-21 11:06:49','01007043150','','','1989-07-05',1,NULL,'female',NULL,NULL),(27,'user','djsaldjsal`','testingtesting','mastia@linuxawy.org','pbkdf2:sha256:260000$R1tgbUFHlP5ojlH6$6d2fea0c85a0b71fca08b519fca6ef7736536e09aace20014c0baf1f59ab25f1',2,2,'2024-04-15 08:55:26','0111877636836821',NULL,NULL,NULL,0,NULL,'male',NULL,NULL);
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

-- Dump completed on 2024-04-18 17:54:06
