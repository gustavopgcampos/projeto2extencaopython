-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.41 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for biblioteca
CREATE DATABASE IF NOT EXISTS `biblioteca` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `biblioteca`;

-- Dumping structure for table biblioteca.emprestimo
CREATE TABLE IF NOT EXISTS `emprestimo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_retirada` date NOT NULL,
  `data_devolucao_prevista` date NOT NULL,
  `data_devolucao_real` date DEFAULT NULL,
  `stats` enum('Y','N') NOT NULL DEFAULT 'Y',
  `livro_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `livro_id` (`livro_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `emprestimo_ibfk_1` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`),
  CONSTRAINT `emprestimo_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table biblioteca.emprestimo: ~0 rows (approximately)

-- Dumping structure for table biblioteca.livro
CREATE TABLE IF NOT EXISTS `livro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `autor` varchar(100) NOT NULL,
  `ano` int NOT NULL,
  `isbn` varchar(13) NOT NULL,
  `stats` enum('Y','N') NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table biblioteca.livro: ~10 rows (approximately)
INSERT INTO `livro` (`id`, `titulo`, `autor`, `ano`, `isbn`, `stats`) VALUES
	(1, 'O Senhor dos Anéis', 'J.R.R. Tolkien', 1954, '9780544003415', 'Y'),
	(2, '1984', 'George Orwell', 1949, '9780451524935', 'Y'),
	(3, 'Dom Casmurro', 'Machado de Assis', 1899, '9788533302273', 'Y'),
	(4, 'A Revolução dos Bichos', 'George Orwell', 1945, '9780451526342', 'Y'),
	(5, 'Cem Anos de Solidão', 'Gabriel García Márquez', 1967, '9780060883287', 'Y'),
	(6, 'Harry Potter e a Pedra Filosofal', 'J.K. Rowling', 1997, '9780747532699', 'Y'),
	(7, 'O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943, '9780156012195', 'Y'),
	(8, 'A Menina que Roubava Livros', 'Markus Zusak', 2005, '9780375842207', 'Y'),
	(9, 'Orgulho e Preconceito', 'Jane Austen', 1813, '9781503290563', 'Y'),
	(10, 'Moby Dick', 'Herman Melville', 1851, '9781503280786', 'Y');

-- Dumping structure for table biblioteca.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(55) NOT NULL,
  `matricula` varchar(55) NOT NULL,
  `email` varchar(55) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table biblioteca.usuario: ~10 rows (approximately)
INSERT INTO `usuario` (`id`, `nome`, `matricula`, `email`) VALUES
	(1, 'Ana Souza', '2025001', 'ana.souza@email.com'),
	(2, 'Bruno Lima', '2025002', 'bruno.lima@email.com'),
	(3, 'Carla Mendes', '2025003', 'carla.mendes@email.com'),
	(4, 'Diego Ferreira', '2025004', 'diego.ferreira@email.com'),
	(5, 'Eduarda Santos', '2025005', 'eduarda.santos@email.com'),
	(6, 'Felipe Almeida', '2025006', 'felipe.almeida@email.com'),
	(7, 'Gabriela Rocha', '2025007', 'gabriela.rocha@email.com'),
	(8, 'Henrique Castro', '2025008', 'henrique.castro@email.com'),
	(9, 'Isabela Martins', '2025009', 'isabela.martins@email.com'),
	(10, 'João Pereira', '2025010', 'joao.pereira@email.com');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
