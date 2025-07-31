# TaskManager (Python and MySQL)
### Prerequisites:
1. MySQL server installed and running
2. Python 3.x installed
3. Install mysql-connector-python package
```
(pip install mysql-connector-python)
```
## Setup MySQL Server and Details
- Host: 127.0.0.1
- User: root
- Password: admin
- Database and Table is created on first use of application.
### Syntax for database and table
```
CREATE DATABASE IF NOT EXISTS TaskManagerDB;
USE TaskManagerDB;
CREATE TABLE IF NOT EXISTS tasks (
  TaskID int NOT NULL AUTO_INCREMENT,
  Title varchar(255) NOT NULL,
  Description varchar(500) DEFAULT NULL,
  DueDate date NOT NULL,
  PriorityLevel enum('Low','Medium','High') DEFAULT 'Low',
  Status enum('Pending','In Progress','Completed') DEFAULT 'Pending',
  CreationTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (TaskID),
  UNIQUE KEY TaskID_UNIQUE (TaskID)
);
```
