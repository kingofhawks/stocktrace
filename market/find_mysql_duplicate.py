# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:lazio_2000@localhost:3306/uportal')

# 查询语句，选出employee表中的所有数据
sql = '''
      select id,batchId,outId,customerId,productId,amount,invoiceMoney,invoiceNum,invoiceDate,mobile,logTime from t_center_invoiceins_import;
      '''

# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)

# 输出employee表的查询结果
print(df)

# duplicate_bool = df.duplicated(subset=['outId', 'productId', 'amount','invoiceMoney','invoiceNum','invoiceDate','mobile'], keep='first')
# duplicate = df.loc[duplicate_bool == True]
duplicate = df[df.duplicated(subset=['outId', 'productId', 'amount','invoiceMoney','invoiceNum','invoiceDate','mobile'], keep='first')]
print(duplicate)
pd.read_sql_query("delete from t_center_invoiceins_import where id='211094'",con=engine)