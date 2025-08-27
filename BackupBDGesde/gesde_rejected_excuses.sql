-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gesde
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rejected_excuses`
--

DROP TABLE IF EXISTS `rejected_excuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rejected_excuses` (
  `id_excuse` int NOT NULL AUTO_INCREMENT,
  `parent_name` varchar(50) NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `grade` varchar(10) NOT NULL,
  `reason` varchar(100) NOT NULL,
  `id_user` int NOT NULL,
  `excuse_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `excuse_duration` varchar(15) DEFAULT NULL,
  `specification` text,
  `file_data` longblob,
  `file_extension` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_excuse`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rejected_excuses`
--

LOCK TABLES `rejected_excuses` WRITE;
/*!40000 ALTER TABLE `rejected_excuses` DISABLE KEYS */;
INSERT INTO `rejected_excuses` VALUES (6,'Wilkins  Figuereo ','Carlos Gómez','4toB','Salud',5,'2025-04-23 04:00:00','1 día','adskjdaskhu',NULL,NULL,'Rechazado','2025-04-23 13:51:28'),(19,'Wilkins  Figuereo ','María Rodríguez','4toA','Salud',5,'2025-05-11 04:00:00','1 día','grthtyh',NULL,NULL,'Rechazado','2025-05-13 08:15:58');
/*!40000 ALTER TABLE `rejected_excuses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-21 12:14:33
