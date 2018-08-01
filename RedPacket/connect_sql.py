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
    os = OperationSQL('trade_central')
    os.execute_sql('SELECT account_name,total_amount FROM trade_central.funds \
    WHERE fund_type=1 AND account_comp_id=1200')
    os.close()
    print(os.get_all_data()[0][1])