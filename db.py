#encoding=utf-8
import pymysql
import pandas as pd

class DB():
    #__host="lsfoo.com"
    __host='116.62.196.228'
    __user='root'
    #__passwd='lsf000000'
    __passwd='qwe1@3'
    __db='mind_tree'
    __port = 3306

    def __init__(self, host=__host, port=__port, db=__db, user=__user, passwd=__passwd, charset='utf8'):
        # 建立连接 
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
    def exec(self,sql):
        ''' 数据库操作 '''
        self.cursor = self.conn.cursor()
        result = 1
        try:
            # 执行sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            result = 0
            print(e)
        finally:
            self.cursor.close()
            return result

    def execMulti(self,sqls):
        ''' 数据库操作 '''
        self.cursor = self.conn.cursor()
        result = 1
        try:
            # 执行sql
            for sql in sqls:
                self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            result = 0
            print(e)
        finally:
            self.cursor.close()
            return result



    def execQuery(self,sql):
        return pd.read_sql(sql=sql,con=self.conn)


