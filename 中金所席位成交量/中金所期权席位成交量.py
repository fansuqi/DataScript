# -*- coding: utf-8 -*-
"""
中金所期权席位成交量爬虫
"""
import time
import pandas as pd


def get_index_option_volume():
    for i in range(1, 13):
        print(i)
        for j in range(1, 32):
            try:
                df = pd.read_csv(f'http://www.cffex.com.cn/sj/ccpm/{year}{i:0>2}/{j:0>2}/{product}_1.csv', encoding='gbk')
            except:
                time.sleep(60)
                df = pd.read_csv(f'http://www.cffex.com.cn/sj/ccpm/{year}{i:0>2}/{j:0>2}/{product}_1.csv', encoding='gbk')
            df.rename({'Unnamed: 4': 'volume', '成交量排名': 'name', '合约系列' : 'symbol'}, axis=1, inplace=True)
            if 'symbol' not in df.columns: # 判断是否正确获得数据
                continue
            df = df[1:] # 去掉首行脏数据
            df['volume'] = df['volume'].astype(int)
            df['symbol'] = df['symbol'].str.replace(' ', '')
            
            # df = df[df['symbol'] == df.groupby('symbol')['volume'].sum().idxmax()]
            df = df[df['symbol'].isin(df.groupby('symbol')['volume'].sum().nlargest(2).index)] # 成交量最大的两个月份
            df = df[['volume', 'symbol', 'name']]
            df['name'] = df['name'].str[:4]
            df = df.groupby('name').sum()[:20]
            df.sort_values('volume', ascending=False, inplace=True)
            rst = df['volume']
            rst.name = f'{year}-{i:0>2}-{j:0>2}'
            yield rst


product = 'IO'
year = 2024
df_rst = pd.concat(get_index_option_volume(), axis=1)
df_rst.index.name = 'date'
df_rst.to_csv(f'/Users/fansuqi/Downloads/{product}{year}.csv', encoding='utf-8')
