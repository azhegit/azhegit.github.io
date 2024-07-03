---
categories:
- 技术
- 数据库
date: 2018-08-05 19:18:38+08:00
tags:
- mysql
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191033396.png
title: mysql修改初始化密码
---
msyql自动修改初始化密码
<!--more-->

1. 获取到mysql初始密码：`cat /var/log/mysqld.log | grep root@localhost: | cut -d " " -f 11`
2. 登录mysql
3. 修改密码强度验证`set global validate_password_policy=0;`
>validate_password_policy
密码强度检查等级，0/LOW、1/MEDIUM、2/STRONG。有以下取值：
Policy                 Tests Performed
0 or LOW               Length
1 or MEDIUM         Length; numeric, lowercase/uppercase, and special characters
2 or STRONG        Length; numeric, lowercase/uppercase, and special characters; dictionary file
默认是1，即MEDIUM，所以刚开始设置的密码必须符合长度，且必须含有数字，小写或大写字母，特殊字符。

4. 修改密码至少要包含的小写字母个数和大写字母个数。`set global validate_password_mixed_case_count=0;`
5. 密码至少要包含的数字个数。`set global validate_password_number_count=0;`
6. 密码至少包含特殊字符：`set global validate_password_special_char_count=0;`
7. 长度验证：`set global validate_password_length=3;`
8. 修改密码为123：`SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123');`
9. 刷新：flush privileges;

执行：mysql -uroot -p$old_db_pass -e 'set global validate_password_policy=0;'报错：
![](https://www.azheimage.top/markdown-img-paste-20180725143034443.png)
需要加`--connect-expired-password`执行

远程访问
grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
flush privileges;

写了一个自动化配置脚本：
```bash
new_db_pass=jkl
old_db_pass=`cat /var/log/mysqld.log | grep root@localhost: | cut -d " " -f 11`
mysql -uroot -p$old_db_pass -e 'set global validate_password_policy=0;' --connect-expired-password;
mysql -uroot -p$old_db_pass -e 'set global validate_password_mixed_case_count=0;' --connect-expired-password;
mysql -uroot -p$old_db_pass -e 'set global validate_password_number_count=0;' --connect-expired-password;
mysql -uroot -p$old_db_pass -e 'set global validate_password_special_char_count=0;' --connect-expired-password;
mysql -uroot -p$old_db_pass -e 'set global validate_password_length=3;' --connect-expired-password;
mysql -uroot -p$old_db_pass -e "alter user 'root'@'localhost' identified by '$new_db_pass';"  --connect-expired-password;
mysql -uroot -p$new_db_pass -e 'flush privileges;' --connect-expired-password;
```

SHOW VARIABLES LIKE 'validate_password%';
