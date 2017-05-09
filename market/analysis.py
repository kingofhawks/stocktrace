import pymongo
import pandas as pd
import json

DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


def sw():
    sw_col = db.sw
    sw_data = sw_col.find()
    df = pd.DataFrame(list(sw_data))
    print(df)
    print('PE min:{}'.format(df['PE'].min()))
    print('PE mean:{}'.format(df['PE'].mean()))
    print('PE max:{}'.format(df['PE'].max()))
    print('PB min:{}'.format(df['PB'].min()))
    print('PB mean:{}'.format(df['PB'].mean()))
    print('PB max:{}'.format(df['PB'].max()))
    df = df.sort_index(by='PB')
    # print df
    df = df.sort_index(by='BargainDate', ascending=False)
    # print df
    latest = df[0:1]
    print(latest)
    # print len(df)
    return df



