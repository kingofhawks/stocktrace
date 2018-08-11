import pandas as pd


# average PE for shanghai http://www.sse.com.cn/market/stockdata/overview/monthly/
def avg_sh_pe(begin_date='1999-12-31'):
    # 上海A股 from 200001
    pe_list = [42.42, 47.99, 49.92, 51.13, 54.02, 55.22, 58.21, 58.13, 54.83, 56.31, 59.89, 59.14,  # year 2000
               59.39, 56.82, 60.88, 60.99, 55.92, 56.55, 49.26, 42.14, 40.61, 38.84, 40.08, 37.59,
               34.31, 35.11, 37.16, 39.08, 38.75, 44.47, 42.4, 43.02, 40.4, 38.23, 36.46, 34.5,
               37.92, 38.2, 38.2, 38.53, 38.28, 36.13, 35.78, 34.37, 32.97, 32.51, 34, 36.64,
               38.91, 40.89, 42.49, 38.95, 28.73, 26.65, 26.49, 25.68, 26.75, 25.34, 25.69, 24.29,
               22.87, 24.99, 22.63, 22.28, 15.66, 15.98, 16.05, 16.92, 16.78, 15.72, 15.63, 16.38,
               17.61, 18, 17.72, 19.42, 19.69, 19.91, 20.03, 20.38, 21.41, 22.86, 26.13, 33.38,
               38.36, 39.62, 44.36, 53.33, 43.42, 42.74, 50.59, 59.24, 63.74, 69.64, 53.79, 59.24,
               49.4, 49.21, 39.45, 42.06, 25.89, 20.64, 20.93, 18.13, 18.68, 14.09, 15.23, 14.86,
               16.26, 17.01, 19.37, 20.21, 22.47, 25.36, 29.47, 23.04, 24.12, 26.03, 27.93, 28.78,
               26.24, 26.91, 27.54, 25.42, 19.93, 18.47, 19.86, 19.85, 20, 22.61, 21.51, 21.6, # 2010
               21.63, 22.56, 22.77, 22.74, 16.34, 16.49, 16.14, 15.42, 14.19, 14.96, 14.17, 13.41,
               14.01, 14.86, 13.86, 14.7, 12.67, 11.9, 11.29, 11.03, 11.25, 11.17, 10.71, 12.29,
               12.97, 12.89, 12.18, 11.89, 11.81, 10.16, 10.26, 10.8, 11.19, 11.05, 11.46, 10.99,
               10.57, 10.73, 10.66, 10.65, 9.76, 9.8, 10.58, 10.68, 11.48, 11.8, 13.14, 15.99,
               15.94, 16.57, 18.97, 22.55, 21.92, 20.92, 18.04, 15.81, 15.1, 16.69, 17.04, 17.61,
               13.73, 13.5, 15.08, 14.75, 14.32, 14.43, 14.77, 15.42, 15.09, 15.73, 16.56, 15.91,
               16.32, 16.83, 16.85, 16.68, 16.49, 16.98, 17.47, 17.99, 18.01, 18.36, 18.1, 18.15,
               19.24, 18.28, 17.77, 17.3, 15.17, 14.07, 14.3, 
               ]

    dates = pd.date_range('20000131', periods=len(pe_list), freq='M')
    # print dates
    # s = pd.Series(pe_list, dates)
    # print s
    s = {'Date': dates, 'PE': pe_list}
    # df = pd.DataFrame(s, index=dates, columns=['PE'])
    # df = pd.DataFrame(s, columns=['Date','PE'])
    # Create DF from dict of list
    df = pd.DataFrame(s)
    if begin_date:
        df = df[df.Date >= begin_date]
    # print 'SH PE min:{} max:{} average:{}'.format(df['PE'].min(), df['PE'].max(), df['PE'].mean())
    # return df['PE'].min(), df['PE'].max(), df['PE'].mean()
    return df