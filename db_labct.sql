-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: labct
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
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('f55a25ea213b');
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
  `nome` varchar(50) NOT NULL,
  `endereco` varchar(150) NOT NULL,
  `bairro` varchar(20) NOT NULL,
  `cidade` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `telefone` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `responsavel` varchar(50) NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  `cnpj` varchar(17) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `filial_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `filial_id` (`filial_id`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`filial_id`) REFERENCES `filial` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (3,'fabio paess x','auau','SAUDADE','dasd','sd','3198689885','fabia@gmail.com','fasas','3165655565','01025025000101',1,'2023-08-01 19:42:32','2023-08-09 16:25:09',1),(5,'FERREIRAS PAEuuu','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','021254125000101',1,'2023-08-04 02:48:31','2023-08-05 23:16:12',1),(6,'jj*****','sdfsfsdf','sfsdfs','sfsdfsd','mg','31989898989','fa@gmail.com','asfsdf','1989898899','02145214000101',2,'2023-08-03 00:00:00','2023-08-08 20:58:54',1),(7,'FERREIRAS PAES 2707','auau','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 15:46:41','2023-08-09 16:24:28',1),(8,'080802023fai','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 15:47:03','2023-08-09 15:52:23',1),(9,'HOJE 0808','auau','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 15:57:51','2023-08-09 15:58:14',3),(10,'OVOS FARIA','auau','dasd','dasd','asd','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',0,'2023-08-09 22:37:35','2023-08-09 22:37:04',3),(11,'fabio paess x','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',0,'2023-08-09 22:37:52','2023-08-09 22:37:04',1),(12,'fabio paess x','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',0,'2023-08-09 22:38:05','2023-08-09 22:37:04',1),(13,'deu certoo','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',0,'2023-08-09 22:38:36','2023-08-09 22:37:04',1),(14,'deu certoo','RUAS DAS AMORAS N100','dasd','dasd','MG','956985698','sdasdasd@gamail.com','fasas','3198659868','02136525000101',1,'2023-08-09 22:49:44','2023-08-10 00:06:45',1);
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
  `nome` varchar(80) NOT NULL,
  `preco` float NOT NULL,
  `validade` date NOT NULL,
  `valor_ultima_compra` float NOT NULL,
  `quantidade_minima` int DEFAULT NULL,
  `obs` text,
  `produto_id` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  `quantidade_op` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `estoque_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `estoque_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `nome` varchar(50) NOT NULL,
  `endereco` varchar(150) NOT NULL,
  `bairro` varchar(20) NOT NULL,
  `cidade` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `responsavel` varchar(50) NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filial`
--

LOCK TABLES `filial` WRITE;
/*!40000 ALTER TABLE `filial` DISABLE KEYS */;
INSERT INTO `filial` VALUES (1,'PDV PAES9','RUA DAS FLORES','VARZEA','BELO HORIZONTE','MG','FABIO154','31989898987','02015025000102',1,'2023-08-01 00:00:00','2023-08-09 17:17:26'),(2,'FABRICA DOS SONHOS','RUA DAS AGUIAS','LAGOA GRANE','FLORAIS','RN','JOAO','76985695548','02365021000112',1,'2023-08-03 00:00:00',NULL),(3,'ALEGRIA CARNES','ESTRADA DAS ROSAS','SAO JOAO','DGALO','MA','RESI','8956988555','23025125000321',1,'2023-08-02 00:00:00','2023-08-09 17:10:08'),(6,'FERREIRAS PAES 2707***99','auau999','dasd','dasd','MG','fasas','3198659868','02136525000101',1,'2023-08-09 17:17:27','2023-08-09 17:17:26'),(7,'FERREIRAS PAES 0908','auau','dasd','dasd','MG','fasas','3198659868','02136525000101',1,'2023-08-09 17:18:03','2023-08-09 17:17:26'),(8,'fabio paess x','RUAS DAS AMORAS N100','dasd','sadasd','MG','fasas','3165655565','02136525000101',0,'2023-08-10 23:05:30','2023-08-10 23:05:30'),(9,'FERREIRAS PAES 1008','RUAS DAS AMORAS N100','dasd','dasd','MG','fasas','3198659868','02136525000101',0,'2023-08-10 23:07:46','2023-08-10 23:05:30');
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
  `nome` varchar(50) NOT NULL,
  `descricao` varchar(200) NOT NULL,
  `endereco` varchar(150) NOT NULL,
  `bairro` varchar(20) NOT NULL,
  `cidade` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `telefone` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `responsavel` varchar(50) NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedor`
--

LOCK TABLES `fornecedor` WRITE;
/*!40000 ALTER TABLE `fornecedor` DISABLE KEYS */;
INSERT INTO `fornecedor` VALUES (1,'OVOS RUTE','OVOS BRANCOS','RUA DAS ALMAS','JUNIA','LAVRAS','MG','32986598587','FARIA@GMAIL.COM','FARIA','32985985874','02012525000111',1,'2023-08-01 00:00:00','2023-08-01 00:00:00');
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
  `nome` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `descricao` varchar(120) DEFAULT NULL,
  `nome` varchar(80) DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `detalhes` varchar(80) DEFAULT NULL,
  `obs` varchar(120) DEFAULT NULL,
  `data` date DEFAULT NULL,
  `produto_id` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `descricao` text NOT NULL,
  `modo_preparo` text NOT NULL,
  `departamento` varchar(20) NOT NULL,
  `rend_kg` float NOT NULL,
  `rend_unid` float NOT NULL,
  `status` tinyint(1) NOT NULL,
  `validade` date NOT NULL,
  `cadastrado_em` date NOT NULL,
  `atualizado_em` date NOT NULL,
  `cliente_id` int NOT NULL,
  `produto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `mixproduto_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `mixproduto_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `cliente_id` varchar(50) NOT NULL,
  `produto_id` varchar(100) NOT NULL,
  `qtde` int NOT NULL,
  `tipo` enum('PedCompraentra','PedProducaosai') NOT NULL,
  `estoque_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estoque_id` (`estoque_id`),
  CONSTRAINT `operacao_ibfk_1` FOREIGN KEY (`estoque_id`) REFERENCES `estoque` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `data_pedido` datetime DEFAULT NULL,
  `data_entrega` date NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `obs` text,
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,500,'2023-08-02 00:00:00','2023-08-10',1,'testan*','2023-08-01 00:00:00','2023-08-03 23:30:01',1,1,1);
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
  `data_pedido` datetime DEFAULT NULL,
  `data_entrega` date NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `obs` text,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `receita_id` int NOT NULL,
  `filial_pdv` int DEFAULT NULL,
  `qtde_pedido` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `filial_pdv` (`filial_pdv`),
  KEY `receita_id` (`receita_id`),
  CONSTRAINT `pedidoproducao_ibfk_1` FOREIGN KEY (`filial_pdv`) REFERENCES `filial` (`id`),
  CONSTRAINT `pedidoproducao_ibfk_2` FOREIGN KEY (`receita_id`) REFERENCES `receita` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidoproducao`
--

LOCK TABLES `pedidoproducao` WRITE;
/*!40000 ALTER TABLE `pedidoproducao` DISABLE KEYS */;
INSERT INTO `pedidoproducao` VALUES (1,'2023-08-06 00:00:00','2023-08-09',1,'sfsdfsdf','2023-08-07 00:00:00','2023-08-07 00:00:00',1,1,NULL);
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
  `nome` varchar(50) NOT NULL,
  `descricao` varchar(150) NOT NULL,
  `quantidade` int DEFAULT NULL,
  `compra_unid` int NOT NULL,
  `peso_pcte` float NOT NULL,
  `valor` double NOT NULL,
  `custo_ultima_compra` float NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  `qrcode` varchar(50) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `fornecedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fornecedor_id` (`fornecedor_id`),
  CONSTRAINT `produto_ibfk_1` FOREIGN KEY (`fornecedor_id`) REFERENCES `fornecedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'OVOS BRANCOS','OVOS DE GRANJA',500,2,0.25,55,51,'32986598988','2125645612156',1,'2023-08-01 00:00:00','2023-08-03 01:37:41',1);
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
  `descricao_mix` text NOT NULL,
  `modo_preparo` text NOT NULL,
  `departamento` varchar(50) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receita`
--

LOCK TABLES `receita` WRITE;
/*!40000 ALTER TABLE `receita` DISABLE KEYS */;
INSERT INTO `receita` VALUES (1,'**RECEITA PAO DE QUEIJO DA VOVO','separe os ingredientes080/','FRIOS',150,100,'2023-08-01',1,'2023-08-01 00:00:00','2023-08-09 21:14:02',1),(2,'faraowqwo','sadasdasdasdasdasdasdasdasdasdada','dsasd',25,2225,'2023-08-01',1,'2023-08-09 16:32:17','2023-08-09 16:31:26',1),(3,'RECEITA PAO DE QUEIJO DA VOVO','ASKJASKFJKALFFKASJFKJASKJA*','dsasd',25,2225,'2023-08-01',0,'2023-08-09 16:32:41','2023-08-09 16:31:26',1),(4,'RECEITA PAO DE QUEIJO DA VOVO','sadasdasdasdasdasdasdasdasdasdada','refrigerado',25,2225,'2023-08-01',0,'2023-08-09 21:19:03','2023-08-09 21:14:02',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `nome` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `cadastrado_em` datetime NOT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `api_key` varchar(100) DEFAULT NULL,
  `empresa` int DEFAULT NULL,
  `cargo` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cargo` (`cargo`),
  KEY `empresa` (`empresa`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `funcao` (`id`),
  CONSTRAINT `usuario_ibfk_2` FOREIGN KEY (`empresa`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'FABIANO9','FABIO@GMAIL.COM','123456',1,1,'2022-12-12 00:00:00','2023-08-11 00:24:01','112121215',NULL,4);
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

-- Dump completed on 2023-08-11  8:56:54
