#!/usr/bin/env bash

sqlite3 ../data.db <<END
CREATE TABLE user (
        empno VARCHAR(4) NOT NULL,
        password VARCHAR(255) NOT NULL,
        firstname_ja VARCHAR(255) NOT NULL,
        lastname_ja VARCHAR(255) NOT NULL,
        firstname_en VARCHAR(255) NOT NULL,
        lastname_en VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
        updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
        deleted INTEGER DEFAULT 0 NOT NULL,
        PRIMARY KEY (empno, password)
)
END
