-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: labct
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('15784abe3176');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `endereco` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bairro` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cidade` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `telefone` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `responsavel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `whatsapp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cnpj` varchar(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `filial_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `filial_id` (`filial_id`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`filial_id`) REFERENCES `filial` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (5,'FERREIRAS PAES 2408-','RUAS DAS AMORAS N100','ROSARIO','MINAS','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','021254125000101',1,'2023-08-04 02:48:31','2023-08-24 16:53:34',8),(6,'fabrica dos sonhos','sdfsfsdf','sfsdfs','sfsdfsd','mg','31989898989','fa@gmail.com','asfsdf','1989898899','02145214000101',0,'2023-08-03 00:00:00','2023-08-28 01:53:06',16),(7,'FERREIRAS PAES 2707','auau','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 15:46:41','2023-08-09 16:24:28',1),(8,'080802023fai','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 15:47:03','2023-08-09 15:52:23',1),(11,'fabio paess 2408','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 22:37:52','2023-08-24 16:53:08',11),(12,'fabio paess x','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 22:38:05','2023-08-11 16:27:04',1),(13,'deu certoo','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',0,'2023-08-09 22:38:36','2023-08-09 22:37:04',1),(15,'REDE SUPER','RUAS DAS PALMEIRAS','NOVO LAVRADO','BELO HORIZONTE','MG','31985698585','SUPER@GMAIL.COM','JOSE','31989858587','02145145000101',1,'2023-08-12 01:24:52','2023-08-12 01:19:41',2),(16,'INDUSTRIA I','CHAC BOA ESEPRANCA','SAUDADES','MATINHOS','MG','32985632521','IND@GMAIL.COM','JOSE','32986587458','01254125000122',1,'2023-08-12 15:15:39','2023-08-12 15:05:39',1),(17,'fabio paess 23082023','RUAS DAS AMORAS N100','SAUDADE','sadasd','asd','956985698','sdasdasd@gamail.com','fasas','3165655565','021254125000101',0,'2023-08-23 20:02:09','2023-08-23 20:02:53',10),(18,'AUGUSTOS OVOS 2408','RUA DA PALMEIRA','NOVO LAVRADO','FLORES','MG','32986598655','INTEGRAL@GMAIL.COM','euler','31978947478','02125412000122',1,'2023-08-24 16:46:38','2023-08-24 16:46:33',2);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `preco` float NOT NULL,
  `validade` date NOT NULL,
  `valor_ultima_compra` float NOT NULL,
  `quantidade_minima` int DEFAULT NULL,
  `obs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `produto_id` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  `quantidade_op` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `estoque_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `estoque_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filial`
--

DROP TABLE IF EXISTS `filial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `endereco` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bairro` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cidade` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `responsavel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `whatsapp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cnpj` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filial`
--

LOCK TABLES `filial` WRITE;
/*!40000 ALTER TABLE `filial` DISABLE KEYS */;
INSERT INTO `filial` VALUES (1,'PDV PAES9','RUA DAS FLORES','VARZEA','BELO HORIZONTE','MG','FABIO154','31989898987','02015025000102',1,'2023-08-01 00:00:00','2023-08-12 01:19:41'),(2,'FABRICA DOS SONHOS','RUA DAS AGUIAS','LAGOA GRANE','FLORAIS','RN','JOAO','76985695548','02365021000112',0,'2023-08-03 00:00:00','2023-08-11 22:36:16'),(3,'ALEGRIA CARNES','ESTRADA DAS ROSAS','SAO JOAO','DGALO','MA','RESI','8956988555','23025125000321',1,'2023-08-02 00:00:00','2023-08-09 17:10:08'),(6,'FERREIRAS PAES 2707***99','auau999','dasd','dasd','MG','fasas','3198659868','02136525000101',0,'2023-08-09 17:17:27','2023-08-12 01:43:08'),(7,'FERREIRAS PAES 0908','auau','dasd','dasd','MG','fasas','3198659868','02136525000101',1,'2023-08-09 17:18:03','2023-08-09 17:17:26'),(8,'fabio paess x','RUAS DAS AMORAS N100','dasd','sadasd','MG','fasas','3165655565','02136525000101',0,'2023-08-10 23:05:30','2023-08-10 23:05:30'),(9,'FERREIRAS PAES 1208','RUAS DAS AMORAS N100','dasd','dasd','MG','fasas','3198659868','02136525000101',0,'2023-08-10 23:07:46','2023-08-12 00:40:43'),(10,'rede paes1','av das acacias','gloria','BELO HORIZONTE','MG','fabio','3198659868','02136525000101',1,'2023-08-12 01:43:08','2023-08-12 01:43:08'),(11,'fabio paess x','RUAS DAS AMORAS N100','SAUDADE','dasd','MG','dasd','3198659868','02136525000101',1,'2023-08-12 19:31:14','2023-08-12 19:27:23'),(16,'FILIAL I','SASFSFA','SAUDADE','MINAS','MG','dasd','3165655565','021254125000101',1,'2023-08-28 00:18:09','2023-08-28 02:17:54');
/*!40000 ALTER TABLE `filial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fornecedor`
--

DROP TABLE IF EXISTS `fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `descricao` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `endereco` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bairro` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cidade` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `telefone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `responsavel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `whatsapp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cnpj` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedor`
--

LOCK TABLES `fornecedor` WRITE;
/*!40000 ALTER TABLE `fornecedor` DISABLE KEYS */;
INSERT INTO `fornecedor` VALUES (1,'OVOS RUTE','OVOS BRANCOS','RUA DAS ALMAS','JUNIA','LAVRAS','MG','32986598587','FARIA@GMAIL.COM','FARIA','32985985874','02012525000111',1,'2023-08-01 00:00:00','2023-08-25 01:25:28'),(5,'FARINHAÇO','FARINHA TRIGO TRAD. / INTEGRAL','AV PRINCIPAL','SAUDADES','MINAS','MG','3198689885','INTEGRAL@GMAIL.COM','LIVIO','3165655565','02125541110020',0,'2023-08-25 01:37:36','2023-08-25 01:32:47'),(6,'MELADOS*','AÇUCAR CRISTAL','RUA DOS FORTES','LAGOA DOURADA','BELEM','PA','71985698854','MELADO@GMAIL.COM','FORMIGAO','71985695211','02412254000111',0,'2023-08-25 16:36:42','2023-08-25 16:33:33');
/*!40000 ALTER TABLE `fornecedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcao`
--

DROP TABLE IF EXISTS `funcao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcao`
--

LOCK TABLES `funcao` WRITE;
/*!40000 ALTER TABLE `funcao` DISABLE KEYS */;
INSERT INTO `funcao` VALUES (2,'COZINHEIRO'),(3,'GERENTE'),(1,'PADEIRO'),(4,'SUPERVISOR');
/*!40000 ALTER TABLE `funcao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nome` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `detalhes` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `obs` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `data` date DEFAULT NULL,
  `produto_id` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (1,'semana/periodo','sdasd',150,'saasda','fsff','2023-08-06',1,NULL);
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mixproduto`
--

DROP TABLE IF EXISTS `mixproduto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mixproduto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cod_prod_mix` int NOT NULL,
  `descricao` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `modo_preparo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `departamento` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rend_kg` float NOT NULL,
  `rend_unid` float NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `validade` date NOT NULL,
  `cadastrado_em` date NOT NULL,
  `atualizado_em` date NOT NULL,
  `cliente_id` int NOT NULL,
  `produto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `mixproduto_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`),
  CONSTRAINT `mixproduto_ibfk_3` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mixproduto`
--

LOCK TABLES `mixproduto` WRITE;
/*!40000 ALTER TABLE `mixproduto` DISABLE KEYS */;
/*!40000 ALTER TABLE `mixproduto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operacao`
--

DROP TABLE IF EXISTS `operacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operacao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `produto_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `qtde` int NOT NULL,
  `tipo` enum('PedCompraentra','PedProducaosai') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estoque_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estoque_id` (`estoque_id`),
  CONSTRAINT `operacao_ibfk_1` FOREIGN KEY (`estoque_id`) REFERENCES `estoque` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operacao`
--

LOCK TABLES `operacao` WRITE;
/*!40000 ALTER TABLE `operacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `operacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `qtde_pedido` int DEFAULT NULL,
  `data_pedido` datetime NOT NULL,
  `data_entrega` date NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `obs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `produto_id` int NOT NULL,
  `fornecedor_id` int DEFAULT NULL,
  `filial_pdv` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `filial_pdv` (`filial_pdv`),
  KEY `fornecedor_id` (`fornecedor_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`filial_pdv`) REFERENCES `filial` (`id`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`fornecedor_id`) REFERENCES `fornecedor` (`id`),
  CONSTRAINT `pedido_ibfk_3` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,500,'2023-08-02 00:00:00','2023-08-10',1,'testan2508','2023-08-01 00:00:00','2023-08-29 00:19:01',2,1,10),(2,500225,'2023-08-26 03:42:09','2023-08-31',1,'testandooo','2023-08-26 03:42:09','2023-08-26 04:34:28',1,1,1),(4,10,'2023-08-26 07:37:45','2023-09-06',1,'testandooo**','2023-08-26 07:37:45','2023-08-26 07:37:14',4,6,2);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidoproducao`
--

DROP TABLE IF EXISTS `pedidoproducao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidoproducao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_pedido` datetime NOT NULL,
  `data_entrega` date NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `obs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `receita_id` int DEFAULT NULL,
  `filial_pdv` int DEFAULT NULL,
  `qtde_pedido` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `filial_pdv` (`filial_pdv`),
  KEY `receita_id` (`receita_id`),
  CONSTRAINT `pedidoproducao_ibfk_1` FOREIGN KEY (`filial_pdv`) REFERENCES `filial` (`id`),
  CONSTRAINT `pedidoproducao_ibfk_2` FOREIGN KEY (`receita_id`) REFERENCES `receita` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidoproducao`
--

LOCK TABLES `pedidoproducao` WRITE;
/*!40000 ALTER TABLE `pedidoproducao` DISABLE KEYS */;
INSERT INTO `pedidoproducao` VALUES (2,'2023-08-26 04:29:15','2023-08-31',1,'kjkdjskd021**9*','2023-08-26 04:29:15','2023-08-26 04:29:10',1,1,250),(3,'2023-08-26 04:29:34','2023-09-07',0,'testandooo888','2023-08-26 04:29:34','2023-08-26 04:34:28',1,2,500),(4,'2023-08-26 13:29:09','2023-08-31',0,'testandooo*9','2023-08-26 13:29:09','2023-08-26 13:27:59',1,1,100),(5,'2023-08-28 19:37:56','2023-08-31',1,'testandooo2808','2023-08-28 19:37:56','2023-08-28 19:36:22',6,2,100);
/*!40000 ALTER TABLE `pedidoproducao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `descricao` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `quantidade` int DEFAULT NULL,
  `compra_unid` int NOT NULL,
  `peso_pcte` float NOT NULL,
  `valor` double NOT NULL,
  `custo_ultima_compra` float NOT NULL,
  `whatsapp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `qrcode` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `fornecedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fornecedor_id` (`fornecedor_id`),
  CONSTRAINT `produto_ibfk_1` FOREIGN KEY (`fornecedor_id`) REFERENCES `fornecedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'OVOS BRANCOS','OVOS DE GRANJA',500,2,0.25,55,51,'32986598988','2125645612156',0,'2023-08-01 00:00:00','2023-08-25 16:33:33',1),(2,'FARINHA INTEGRAL A GRANEL','FARINHA TRIGO TRAD. / INTEGRAL',450,25,100,250,225,'3198659868','899989855545454',1,'2023-08-25 01:46:06','2023-08-25 01:32:47',5),(4,'deu certoo2408','FARINHA TRIGO TRAD',1254,25,100,2541,16,'3165655565','899989855545454',0,'2023-08-25 02:06:48','2023-08-25 02:13:15',1),(5,'AÇUCAR CRISTAL*','A GRANEL PCT 50KG',10,25,250,21,18,'3165655565','1215464654',0,'2023-08-25 16:37:19','2023-08-25 16:33:33',6);
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receita`
--

DROP TABLE IF EXISTS `receita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receita` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descricao_mix` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `modo_preparo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `departamento` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rend_kg` float NOT NULL,
  `rend_unid` float NOT NULL,
  `validade` date NOT NULL,
  `status` int DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `produto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `receita_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receita`
--

LOCK TABLES `receita` WRITE;
/*!40000 ALTER TABLE `receita` DISABLE KEYS */;
INSERT INTO `receita` VALUES (1,'RECEITA PAO DE QUEIJO DA VOVO','separe os ingredientes','FRIOS',150,100,'2023-08-01',0,'2023-08-01 00:00:00','2023-08-11 22:25:49',1),(6,'ROSCA RECHEADA','ACOMPANHAR RECEITA','PANIFICACAO',25,2,'2023-08-30',1,'2023-08-26 13:38:19','2023-08-26 13:36:20',1),(7,'ROSCA RECHEADA','VER DESCRICAO MIX','PANIFICACAO',10,2,'2023-09-07',1,'2023-08-28 19:37:09','2023-08-28 19:36:22',2);
/*!40000 ALTER TABLE `receita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receita_filial`
--

DROP TABLE IF EXISTS `receita_filial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receita_filial` (
  `receita_id` int NOT NULL,
  `filial_id` int NOT NULL,
  PRIMARY KEY (`receita_id`,`filial_id`),
  KEY `filial_id` (`filial_id`),
  CONSTRAINT `receita_filial_ibfk_1` FOREIGN KEY (`filial_id`) REFERENCES `filial` (`id`),
  CONSTRAINT `receita_filial_ibfk_2` FOREIGN KEY (`receita_id`) REFERENCES `receita` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receita_filial`
--

LOCK TABLES `receita_filial` WRITE;
/*!40000 ALTER TABLE `receita_filial` DISABLE KEYS */;
INSERT INTO `receita_filial` VALUES (1,1);
/*!40000 ALTER TABLE `receita_filial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receita_produto`
--

DROP TABLE IF EXISTS `receita_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receita_produto` (
  `receita_id` int NOT NULL,
  `produto_id` int NOT NULL,
  PRIMARY KEY (`receita_id`,`produto_id`),
  UNIQUE KEY `receita_id` (`receita_id`),
  UNIQUE KEY `produto_id` (`produto_id`),
  CONSTRAINT `receita_produto_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`),
  CONSTRAINT `receita_produto_ibfk_2` FOREIGN KEY (`receita_id`) REFERENCES `receita` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receita_produto`
--

LOCK TABLES `receita_produto` WRITE;
/*!40000 ALTER TABLE `receita_produto` DISABLE KEYS */;
/*!40000 ALTER TABLE `receita_produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `senha` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `api_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `empresa` int DEFAULT NULL,
  `cargo` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cargo` (`cargo`),
  KEY `empresa` (`empresa`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `funcao` (`id`),
  CONSTRAINT `usuario_ibfk_2` FOREIGN KEY (`empresa`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'FABIANO2408','FABIO@GMAIL.COM','123456',1,1,'2022-12-12 00:00:00','2023-08-24 16:46:33','112121215',5,3),(2,'CHARLES JOSE','fabia@gmail.com','$pbkdf2-sha256$29000$u7cWIoSwFsJ4b01prdW6Nw$Ut2tDFYgVB7/VcUL2UA2ncx8Tf892g0Ao0iQgjoNy5Q',0,1,'2023-08-24 16:41:29','2023-08-24 16:50:41',NULL,6,3),(4,'FELIPE SANTOS','SANTOS@GMAIL.COM','$pbkdf2-sha256$29000$aG2tVSplLEXoXSvFGANASA$k638R.wBXdhxgAHFPoXnmspGfGPZWagamSoRBNYkpDA',1,0,'2023-08-24 22:21:43','2023-08-24 22:21:04',NULL,6,4);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-29 22:49:16
