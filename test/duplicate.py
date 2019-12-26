# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:lazio_2000@localhost:3306/uportal2')

# 查询语句，选出employee表中的所有数据
sql = '''
      select id,batchId,outId,customerId,refInsId,productId,amount,invoiceMoney,invoiceNum,invoiceDate,mobile,logTime from t_center_invoiceins_import;
      '''

# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)

# 输出employee表的查询结果
print(len(df))

# duplicate_bool = df.duplicated(subset=['outId', 'productId', 'amount','invoiceMoney','invoiceNum','invoiceDate','mobile'], keep='first')
# duplicate = df.loc[duplicate_bool == True]
duplicate = df[df.duplicated(subset=['outId', 'productId', 'amount','invoiceMoney','invoiceNum','invoiceDate','mobile'], keep=False)]
print(duplicate)
# 找出正常的数据
removed = 0
for index, row in duplicate.iterrows():
    ins_id = row['refInsId']
    row_id = row['id']
    if ins_id:
        try:
            sql = "select * from t_center_vs_insout where insId='"+str(ins_id)+"'"
            # print(sql)
            df1 = pd.read_sql_query(sql, con=engine)

            sql2 = "select * from t_center_invoiceins where id='" + str(ins_id) + "'"
            df2 = pd.read_sql_query(sql2, con=engine)
            if len(df1)> 0 and len(df2) >0:
                print(row_id, index, ins_id)
                removed += 1
                duplicate = duplicate.drop(index=index)
        except:
            continue
print(duplicate)
print('removed', removed)
# for index, row in duplicate.iterrows():
#     row_id = row['id']
#     try:
#         sql = "delete from t_center_invoiceins_import where id='"+str(row_id)+"'"
#         print(sql)
#         pd.read_sql_query(sql, con=engine)
#     except:
#         continue
# sql = "delete from t_center_invoiceins_import where id='217055'"
# print(sql)
# pd.read_sql_query(sql,con=engine)