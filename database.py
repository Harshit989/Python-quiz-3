CREATE DATABASE IF NOT EXISTS quiz_app;

USE quiz_app;

-- Create a table for users
CREATE TABLE IF NOT EXISTS users (
    reg_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Create a table for questions
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    options JSON NOT NULL,
    correct_answer CHAR(1) NOT NULL
);

-- Create a table for quiz attempts
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_id VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    FOREIGN KEY (reg_id) REFERENCES users (reg_id)
);
