#!/usr/bin/env bash

sqlite3 ../data.db <<END
DELETE FROM user;
INSERT INTO user (empno, firstname_ja, lastname_ja, firstname_en, lastname_en, email) VALUES ('0411', '大悟', '中島', 'taigo', 'nakajima', 't.n@example.com');
INSERT INTO user (empno, firstname_ja, lastname_ja, firstname_en, lastname_en, email) VALUES ('0512', '恭平', '竹下', 'kyohei', 'takeshita', 'k.t@example.com');
END
