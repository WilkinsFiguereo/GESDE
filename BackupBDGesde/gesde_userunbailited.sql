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
-- Table structure for table `userunbailited`
--

DROP TABLE IF EXISTS `userunbailited`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userunbailited` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `idcard` varchar(20) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userunbailited`
--

LOCK TABLES `userunbailited` WRITE;
/*!40000 ALTER TABLE `userunbailited` DISABLE KEYS */;
INSERT INTO `userunbailited` VALUES (1,'Wilkins Radhames Figuereo Jimenez','admin','(000)-000-0000','000-0000000-0','2025-04-30 18:05:32'),(6,'Yeraldo Domingo','parent','(829)-840-4501','333-3333333-3','2025-02-24 14:14:14'),(27,'twilio','parent','(545)-646-5475','123-2342343-4','2025-04-21 19:15:50'),(29,'twilio3','parent','(192)-309-1203','390-1284309-1','2025-04-21 19:21:18'),(31,'Twilio5','parent','(643)-654-6564','345-3453454-6','2025-04-21 19:27:47'),(32,'Twilio6','parent','(123)-738-9721','217-3981273-9','2025-04-21 19:34:09');
/*!40000 ALTER TABLE `userunbailited` ENABLE KEYS */;
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
