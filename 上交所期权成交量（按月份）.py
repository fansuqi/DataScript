"""
从Wind获取ETF期权每天的成交量（按月份）
"""

import pandas as pd

from WindPy import w
w.start()


start_date = '2024-06-21'
end_date = '2024-07-20'
exchange = 'sse'

for underlying in ['510050.SH', '510300.SH', '510500.SH']:
    wind_sql = 'startdate=%s;enddate=%s;exchange=%s;windcode=%s'
    err_code, df = w.wset('ssetradingstatisticsbymonth',
                          wind_sql % (start_date, end_date, exchange, underlying), 
                          usedf=True)
    
    df_rst = pd.pivot(df, index='date', columns='expiredate', values='daily_volume')
    print(df_rst)
    df_rst.to_csv('E:/%s.csv' % underlying)
