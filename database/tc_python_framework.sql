-- Database
CREATE DATABASE tc_python_framework;


-- Table
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT (CURRENT_DATE),
  `updated_at` datetime DEFAULT (CURRENT_DATE),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- User table data
INSERT INTO tc_python_framework.`user` (first_name,last_name,email,phone,password,`role`,updated_at,created_at) VALUES
   ('User','One','userone@targetclose.com','9988776655','3ffb4015404b4444251a5d94f08df277414924c03742b432066c0fe5ef2a6fd2','user',NOW(),NOW()),
   ('User','Two','usertwo@targetclose.com','9988776644','3ffb4015404b4444251a5d94f08df277414924c03742b432066c0fe5ef2a6fd2','user',NOW(),NOW()),
   ('Admin','User','admin@targetclose.com','9988776633','3ffb4015404b4444251a5d94f08df277414924c03742b432066c0fe5ef2a6fd2','admin',NOW(),NOW());
