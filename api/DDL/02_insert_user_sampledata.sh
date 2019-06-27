#!/usr/bin/env bash

sqlite3 ../data.db <<END
DELETE FROM user;
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0411', 'pw0411', '大悟', '中島', 'taigo', 'nakajima', 'taigo.nakajima@example.com', 1);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0512', 'pw0512', '恭平', '竹下', 'kyohei', 'takeshita', 'kyohei.takeshita@example.com', 0);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0424', 'pw0424', '光輝', '宮脇', 'kouki', 'miyawaki', 'kouki.miyawaki@example.com', 0);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0623', 'pw0623', '昭人', '吉村', 'akito', 'yoshimura', 'akito.yoshimura@example.com', 0);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0999', 'pw0999', '卓也', '藤本', 'takuya', 'fujimoto', 'takuya.fujimoto@example.com', 0);
INSERT INTO user (empno, password, firstname_ja, lastname_ja, firstname_en, lastname_en, email, admin) VALUES ('0212', 'pw0212', '黄', '聖浩', 'songho', 'hwang', 'songho.hwang@example.com', 1);
END
