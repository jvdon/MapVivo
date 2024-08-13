SET GLOBAL innodb_monitor_enable='cpu%';

use vivo;
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    ping FLOAT DEFAULT 0,
    checked_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
