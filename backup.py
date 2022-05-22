import os

#执行mysqldump命令，数据库备份文件暂时存放的位置
if not os.path.exists('mysqldb_backup'):
    os.mkdir('mysqldb_backup')
os.chdir('mysqldb_backup')

#执行mysqldump命令 账号、密码、ip、端口、数据库名 需要根据自己情况调整
os.system("mysqldump -u root -p231655 -h 127.0.0.1 csp > mysql_backup.sql")


