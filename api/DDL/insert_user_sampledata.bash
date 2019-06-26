#!/usr/bin/env bash

sqlite3 ../data.db <<END
DELETE FROM user;
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0411', 'p0411', '大悟', '中島', 'taigo', 'nakajima', 't.n@example.com', 1);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0512', 'p0512', '恭平', '竹下', 'kyohei', 'takeshita', 'k.t@example.com', 0);
END
