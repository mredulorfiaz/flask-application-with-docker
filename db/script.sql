CREATE DATABASE IF NOT EXISTS flaskDB;
USE flaskDB;
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    mobile VARCHAR (15) UNIQUE,
    isDeleted TINYINT DEFAULT 0
);
