import pymysql

"""
连接数据库MYSQL，增删改查
"""
class OperationSQL:

    def __init__(self,database):
        self.db = pymysql.connect('172.16.1.125','root','root&123',database,charset='utf8')
        self.cursor = self.db.cursor()

    def execute_sql(self,sql):
        '''执行SQL语句'''
        self.cursor.execute(sql)

    def get_all_data(self):
        '''获取表所有数据'''
        results = self.cursor.fetchall()
        self.close()
        return results



    def close(self):
        '''关闭数据库'''
        self.cursor.close()

if __name__ == "__main__":
    OS = OperationSQL()
    mobile = 13634659752
    OS.execute_sql("SELECT * FROM baseinfo_company WHERE admin_person_mobile = %s"%mobile)
    print(OS.get_all_data()[0][0])
