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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `idcard` varchar(40) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `profile_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idcard` (`idcard`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'Wilberto Jaime','parent','(849)-800-2000','222-2222222-2','29','2025-04-19 01:47:29',NULL),(5,'Wilkins  Figuereo ','parent','(121)-212-1212','121-2121212-1','scrypt:32768:8:1$jFG1eTYJYGBAs4JF$fe237ca21717d2d6c2c57465a644ad13e5dbefb215cb1e573ba52ad4af7ea608988b6e9de726429ab827720ce455cd0d389997dcda0552b0539a912f6918dc1a','2025-05-06 03:06:29','1.png'),(7,'Nombre','administration','(555)-555-5555','555-5555555-5','scrypt:32768:8:1$DyaFrMxT4KIAsFFX$a906eb1fafcd404e0711a2cb9bb3c1272b4b5ea387a2104f6d2306601b0a30f378275d661f443d62923a4dd4069206e98fbbfabe1477094a1c221e0c9ad83d34','2025-05-07 05:43:44',NULL),(12,'Rijo','teacher','(444)-444-4444','444-4444444-4','scrypt:32768:8:1$WObWw7GK1TqdiNPb$bd41297235e2dec06aa6d9290ef6abf847fb73e8c38b4961c99cbaa927aab6b83ba62302f16ab4c9ccccf304707eb9fc0c326646f9c7d016721ccbbcf6c7fc9b','2025-05-13 12:28:19','2.png'),(13,'Miguel','teacher','(888)-888-8888','888-8888888-8','8','2025-03-15 20:40:50',NULL),(14,'Chinchin','teacher','(657)-576-4564','454-6465475-4','uyiu','2025-03-15 20:41:16',NULL),(15,'Rosalba','teacher','(646)-654-3543','765-7658765-8','54574','2025-03-15 20:41:42',NULL),(17,'Darwinfwe','teacher','(214)-912-9412','304-1412312-9','124=12312==31','2025-03-15 20:42:58',NULL),(18,'Myke Tower','teacher','(219)-301-2803','012-9301231-9','JonKing','2025-03-15 20:43:38',NULL),(23,'Sebastian Gutierrez','admin','(100)-000-0000','100-0000000-0','101','2025-04-04 15:28:18',NULL),(24,'Darwin','teacher','(245)-253-4534','432-4536547-5','123','2025-05-12 02:31:10',NULL),(25,'Joerlin Quezada','parent','(193)-039-0290','300-0000000-0','123','2025-04-19 01:43:50',NULL),(26,'imgu88u9','parent','(444)-444-4444','444-4444444-5','123','2025-04-21 23:45:37','<FileStorage: \'\' (\'application/octet-stream\')>'),(28,'twilio2','parent','(234)-920-4923','239-0423040-2','348937','2025-04-21 19:18:21','ASSETS/IMG/GenericImg/usuario.png'),(30,'Twilio4','parent','(384)-983-8949','328-0840329-4','1398109','2025-04-21 19:22:30','ASSETS/IMG/GenericImg/usuario.png'),(35,'Twilio6','parent','(123)-738-9721','217-3981273-4','73289','2025-04-21 19:36:47','ASSETS/IMG/GenericImg/usuario.png'),(36,'Twilio9','parent','(328)-490-2384','234-2342342-3','54532','2025-04-21 19:38:44','ASSETS/IMG/GenericImg/usuario.png'),(37,'Twilio10','parent','(356)-775-6756','234-2342342-7','54532','2025-04-21 19:39:51','ASSETS/IMG/GenericImg/usuario.png'),(38,'twilio11','parent','(290)-293-4230','232-3423423-4','2p13i02193','2025-04-21 19:42:00','ASSETS/IMG/GenericImg/usuario.png'),(39,'twilio12','parent','(290)-293-4230','232-3423423-5','2p13i02193','2025-04-21 19:45:11','ASSETS/IMG/GenericImg/usuario.png'),(40,'Nombre mas largo para probar','parent','(349)-304-8398','482-9038028-9','1213','2025-04-21 20:57:45','ASSETS/IMG/GenericImg/usuario.png'),(41,'Sebastian Gutierrez ','parent','(231)-273-1862','000-0000000-5','35','2025-04-22 12:41:15','ASSETS/IMG/GenericImg/usuario.png'),(42,'Update','parent','(243)-809-3248','723-9472893-4','update','2025-04-24 02:32:11','ASSETS/IMG/GenericImg/usuario.png'),(43,'min','administration','(654)-645-6456','657-5476575-6','31','2025-04-25 03:55:14','ASSETS/IMG/GenericImg/usuario.png'),(44,'cifrado','administration','(913)-021-3801','238-1032109-3','scrypt:32768:8:1$QrNgdqMl4pSnp0Or$6c40c8f23dc3b972587b67ff62eca2ceaa1245684ccdc8bc86f928ebbc7e0daac6eb2ca649101716113080315e48ff8e89208c21c1da01e847a7569b86307393','2025-05-06 02:44:43','ASSETS/IMG/GenericImg/usuario.png'),(46,'cifrado','administration','(913)-021-3801','238-1032109-8','scrypt:32768:8:1$2wiwHIju3i9iY8NJ$23a9042ca5999675189b39152f6735e12b6b5bc299e4c4caf87ade04fa87315bf1dacd45cbd26e789c31d0cb81eda0dfcb37ce4ee625fb90136acd533a8e4f63','2025-05-06 02:44:59','ASSETS/IMG/GenericImg/usuario.png'),(47,'Admin','admin','(000)-000-0000','000-0000000-0','scrypt:32768:8:1$kjebLzAyf9Z1QpLC$d8cf3e0830ccf254807c455f7466536cbb890bf0bb1bea40df537298e8e2f58337a22bccbc6e01a592dbeb6ff95c18a99ef279a1989122a2ff9d6b870fd94628','2025-05-06 03:36:24','cuphead.png'),(49,'Prueba ninos','parent','(111)-111-1111','111-1111111-1','scrypt:32768:8:1$nMZcS239TiMwsv4n$d3aede726d6a9ee7b17b27493056982ce61ad90b906de840d4e920fcf55cfa22c2cf9c7540bc1ad8ec553437f3fa297876b6b72a60754fbe27e95d48cd04eb6c','2025-05-17 20:23:38','ASSETS/IMG/GenericImg/usuario.png'),(51,'Prueba ninos 2','parent','(111)-111-1112','111-1111111-2','scrypt:32768:8:1$emDpnEfTT78MusZ5$6bcf5a07b4531240b7b9d97f05d3fdcb9b04e42b444efb14fdb4f016766e0a647cf11d9c44cc4d1b71d54ad4bbaf01fc1e002d051ce6bb25338f3ba586220b5f','2025-05-17 20:26:23','ASSETS/IMG/GenericImg/usuario.png');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
