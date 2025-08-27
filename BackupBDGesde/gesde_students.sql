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
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `grade` varchar(50) NOT NULL,
  `teacher_id` int DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teacher` (`teacher_id`),
  KEY `fk_parent_id` (`parent_id`),
  CONSTRAINT `fk_parent` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (2,'María Rodríguez','4toA',NULL,NULL),(3,'Carlos Gómez','4toB',NULL,NULL),(4,'Ana Fernández','4toB',NULL,NULL),(5,'Miguel Torres','5toA',NULL,NULL),(6,'Laura Sánchez','5toA',NULL,NULL),(7,'José Ramírez','5toB',NULL,NULL),(8,'Sofía Díaz','5toB',NULL,NULL),(9,'Ricardo Herrera','6toA',NULL,NULL),(10,'Elena Vargas','6toA',NULL,NULL),(12,'María López','4toA',NULL,NULL),(13,'Carlos Rodríguez','4toA',NULL,NULL),(14,'Ana Gómez','4toB',NULL,NULL),(15,'Pedro Fernández','4toB',NULL,NULL),(16,'Lucía Sánchez','4toB',NULL,NULL),(17,'Miguel Torres','4toC',NULL,NULL),(18,'Sofía Ramírez','4toC',NULL,NULL),(19,'Diego Vargas','4toC',NULL,NULL),(20,'Valentina Herrera','4toD',NULL,NULL),(21,'Emilio Castro','4toD',NULL,NULL),(22,'Camila Morales','4toD',NULL,NULL),(23,'José Ríos','5toA',NULL,NULL),(24,'Martina Navarro','5toA',NULL,NULL),(25,'Samuel Ortega','5toA',NULL,NULL),(26,'Elena Mendoza','5toB',NULL,NULL),(27,'Andrés Figueroa','5toB',NULL,NULL),(28,'Renata Paredes','5toB',NULL,NULL),(29,'Gabriel Suárez','5toC',NULL,NULL),(30,'Fernanda León','5toC',NULL,NULL),(31,'Ricardo Guzmán','5toC',NULL,NULL),(32,'Victoria Peña','5toD',NULL,NULL),(33,'Hugo Salazar','5toD',NULL,NULL),(34,'Daniela Cabrera','5toD',NULL,NULL),(35,'Sebastián Rojas','6toA',NULL,NULL),(36,'Isabella Méndez','6toA',NULL,NULL),(37,'Mateo Aguilar','6toA',NULL,NULL),(38,'Olivia Domínguez','6toB',NULL,NULL),(39,'Felipe Espinoza','6toB',NULL,NULL),(40,'Regina Villalobos','6toB',NULL,NULL),(41,'Alejandro Castillo','4toA',NULL,NULL),(42,'Mariana Vargas','4toA',NULL,NULL),(43,'Francisco Ríos','4toA',NULL,NULL),(44,'Natalia Herrera','4toB',NULL,NULL),(45,'Javier Mendoza','4toB',NULL,NULL),(46,'Andrea Suárez','4toB',NULL,NULL),(47,'Fernando Morales','4toC',NULL,NULL),(48,'Paula Ortega','4toC',NULL,NULL),(49,'Luis Guzmán','4toC',NULL,NULL),(50,'Carmen Espinoza','4toD',NULL,NULL),(51,'Santiago Paredes','4toD',NULL,NULL),(52,'Lorena Figueroa','4toD',NULL,NULL),(53,'Raúl Cabrera','5toA',NULL,NULL),(54,'Patricia Peña','5toA',NULL,NULL),(55,'Iván Salazar','5toA',NULL,NULL),(56,'Beatriz Domínguez','5toB',NULL,NULL),(57,'Ernesto Navarro','5toB',NULL,NULL),(58,'Carolina León','5toB',NULL,NULL),(59,'Tomás Rodríguez','5toC',NULL,NULL),(60,'Silvia Torres','5toC',NULL,NULL),(61,'Héctor Fernández','5toC',NULL,NULL),(62,'Rocío Gómez','5toD',NULL,NULL),(63,'Esteban Sánchez','5toD',NULL,NULL),(64,'Julia Castro','5toD',NULL,NULL),(65,'Agustín Ramírez','6toA',NULL,NULL),(66,'Elisa Aguilar','6toA',NULL,NULL),(67,'Maximiliano Méndez','6toA',NULL,NULL),(68,'Clara López','6toB',NULL,NULL),(69,'Gustavo Pérez','6toB',NULL,NULL),(70,'Valeria Rojas','6toB',NULL,NULL),(71,'Juan Pérez','5to B',12,NULL),(72,'Juan Pérez','5toB',12,NULL),(73,'Juan Jose','5toB',12,NULL),(74,'Prueba estudiante','6toB',14,NULL),(75,'Wilberto','5toB',NULL,NULL),(76,'Wilberto','5toB',NULL,NULL),(77,'Wilberto','5toB',NULL,NULL),(78,'Wilkin','4toD',NULL,NULL),(79,'Jaimito Luperon','5toD',NULL,NULL),(80,'Lioner Messi','4toC',NULL,NULL),(81,'Bryan Batista','4toD',NULL,NULL),(82,'Bryan Batista ll','5toD',NULL,NULL),(83,'Bryan Batista ll','5toD',NULL,NULL),(84,'Wilkins Radhames','5toF',NULL,NULL),(85,'Justin ciego','4toF',NULL,NULL),(86,'Bryan Batista','5toF',NULL,NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
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
