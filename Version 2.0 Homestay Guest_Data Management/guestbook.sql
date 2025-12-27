CREATE DATABASE connector_db;

USE connector_db;

CREATE TABLE guestbook (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    purpose VARCHAR(50),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);