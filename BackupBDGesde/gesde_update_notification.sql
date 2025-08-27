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
-- Table structure for table `update_notification`
--

DROP TABLE IF EXISTS `update_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_notification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  `detail` text,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `update_notification`
--

LOCK TABLES `update_notification` WRITE;
/*!40000 ALTER TABLE `update_notification` DISABLE KEYS */;
INSERT INTO `update_notification` VALUES (1,'Agregaro','Se ha agregado el ususario Update rol: parent','2025-04-23 22:32:11'),(2,'Agregaro','Se ha un nuevo grado: 4toF','2025-04-23 22:48:48'),(3,'Agregaro','Se ha asignado al profesor 12 el dia: miércoles para el grado: 5toF','2025-04-23 22:51:33'),(4,'Agregaro','Se ha asignado al profesor 12 el dia: jueves para el grado: 4toF','2025-04-23 22:51:48'),(5,'Agregaro','Se ha un nuevo estudiante Wilkins Radhames grado: 5toF','2025-04-23 22:53:14'),(6,'Agregaro','Se ha un nuevo estudiante Justin ciego grado: 4toF','2025-04-23 22:54:05'),(7,'Actualizacion','Se ha actualizado el usuario: Wilkin  Figuereo ','2025-04-24 11:16:25'),(8,'Editado','Se ha editado el usuario: Wilkins  Figuereo ','2025-04-24 12:08:09'),(9,'Agregaro','Se ha agregado un nuevo usuario ususario min rol: administration','2025-04-24 23:55:14'),(10,'Agregaro','Se ha un nuevo estudiante Bryan Batista grado: 5toF','2025-04-30 17:37:35'),(11,'Agregaro','Se ha agregado un nuevo usuario ususario cifrado rol: administration','2025-05-05 22:44:43'),(12,'Agregaro','Se ha agregado un nuevo usuario ususario cifrado rol: administration','2025-05-05 22:44:59'),(13,'Agregaro','Se ha agregado un nuevo usuario ususario Admin rol: admin','2025-05-05 22:53:03'),(14,'Deshabilitado','Se ha deshabilitado el ususario Wilkins Radhames Figuereo Jimenez','2025-05-05 22:53:17'),(15,'Editado','Se ha editado el usuario: Admin','2025-05-05 22:54:23'),(16,'Editado','Se ha editado el usuario: Wilkins  Figuereo ','2025-05-05 23:06:29'),(17,'Editado','Se ha editado el usuario: Nombre','2025-05-07 01:43:44'),(18,'Editado','Se ha editado el usuario: Rijo','2025-05-07 02:06:41'),(19,'Eliminación','Estudiante eliminado con ID: 1','2025-05-07 10:53:45'),(20,'Eliminación','Estudiante eliminado con ID: 11','2025-05-07 10:54:00'),(21,'Editado','Se ha editado el usuario: Chinchin','2025-05-11 22:30:45'),(22,'Editado','Se ha editado el usuario: Darwin','2025-05-11 22:31:10'),(23,'Horario eliminado','Se eliminó el horario del profesor 13 para el grado 5toF.','2025-05-12 23:43:45'),(24,'Horario eliminado','Se eliminó el horario del profesor 14 para el grado None.','2025-05-12 23:45:24'),(25,'Horario eliminado','Se eliminó el horario del profesor 13 para el grado None.','2025-05-12 23:45:30'),(26,'Horario eliminado','Se eliminó el horario del profesor 12 para el grado None.','2025-05-12 23:45:37'),(27,'Editado','Se ha editado el usuario: Rijo','2025-05-13 08:28:19'),(28,'Editado','Se ha editado el usuario: Prueba ninos 2','2025-05-17 17:07:06'),(29,'Editado','Se ha editado el usuario: Wilkins  Figuereo ','2025-05-19 00:29:47'),(30,'Editado','Se ha editado el usuario: Wilkins  Figuereo ','2025-05-19 01:06:44'),(31,'Asignado','Se ha asignado al profesor 14 el día: martes para el grado: 6toB','2025-05-19 08:54:30'),(32,'Asignado','Se ha asignado al profesor 14 el día: martes para el grado: 6toB','2025-05-19 08:58:15');
/*!40000 ALTER TABLE `update_notification` ENABLE KEYS */;
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
