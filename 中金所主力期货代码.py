"""
获取主力股指期货合约代码
"""

import pandas as pd

from WindPy import w
w.start()


start_date = '2023-01-01'
end_date = '2024-08-24'


def get_main_contract(fut_product):
    err_code, df = w.wsd('%s.CFE' % fut_product, 'trade_hiscode', 
                         start_date, end_date, '', usedf=True)
    return df['TRADE_HISCODE'].str.replace('.CFE', '')


lst_product = ['IC', 'IH', 'IF', 'IM']
df_rst = pd.concat([get_main_contract(product) for product in lst_product], axis=1)
df_rst.columns = lst_product
df_rst.to_csv('F:/fut_main_contract.csv')
