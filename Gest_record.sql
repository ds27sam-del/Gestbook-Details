CREATE DATABASE GestBook_record
    DEFAULT CHARACTER SET = 'utf8mb4';

use GestBook_record

create TABLE Gest_personal_record(
    id INT(4) PRIMARY KEY AUTO_INCREMENT,
    number_of_members INT,
    name VARCHAR(30),
    Foreign Key (addhar_no) REFERENCES (Gest_record(addhar_no)),
    age INT(3),
    phone_no int(11),
    E_main VARCHAR(30),
    address VARCHAR(50)
)

create TABLE Gest_record(
    id INT(4) PRIMARY KEY AUTO_INCREMENT,
    addhar_no int(11),
    number_of_members int,
    room_type VARCHAR(10),
    room_no int(5),
    room_checkin DATETIME,
    room_checkout DATETIME,
    number_mambers int(4)
)