#!/usr/bin/env bash

sqlite3 ../data.db <<EOF
CREATE TABLE user (
        empno VARCHAR(4) NOT NULL,
        password VARCHAR(255) NOT NULL,
        firstname_ja VARCHAR(255) NOT NULL,
        lastname_ja VARCHAR(255) NOT NULL,
        firstname_en VARCHAR(255) NOT NULL,
        lastname_en VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        updated_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        admin INTEGER DEFAULT 0 NOT NULL,
        deleted INTEGER DEFAULT 0 NOT NULL,
        PRIMARY KEY (empno)
);
CREATE TRIGGER trigger_user_updated_at AFTER UPDATE ON user
BEGIN
    UPDATE user SET updated_at = DATETIME('now', 'localtime') WHERE empno == NEW.empno;
END;

CREATE TABLE division (
        division_id INTEGER NOT NULL,
        division_code VARCHAR(16) NOT NULL,
        division_name_ja VARCHAR(80) NOT NULL,
        division_name_en VARCHAR(80) NOT NULL,
        created_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        updated_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        deleted INTEGER DEFAULT 0 NOT NULL,
        PRIMARY KEY (division_id),
        UNIQUE (division_id)
);
CREATE TRIGGER trigger_division_updated_at AFTER UPDATE ON division
BEGIN
    UPDATE division SET updated_at = DATETIME('now', 'localtime') WHERE division_id == NEW.division_id;
END;

CREATE TABLE user_division (
        empno VARCHAR(4) NOT NULL,
        division_id INTEGER NOT NULL,
        admin INTEGER DEFAULT 0 NOT NULL,
        created_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        updated_at DATETIME DEFAULT (DATETIME('now', 'localtime')) NOT NULL,
        deleted INTEGER DEFAULT 0 NOT NULL,
        PRIMARY KEY (empno, division_id)
);
CREATE TRIGGER trigger_user_division_updated_at AFTER UPDATE ON user_division
BEGIN
    UPDATE user_division SET updated_at = DATETIME('now', 'localtime') WHERE empno == NEW.empno AND division_id == NEW.division_id;
END;
EOF
