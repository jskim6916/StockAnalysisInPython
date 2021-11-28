import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer
from Investar import DBUpdaterEx

dbu = DBUpdaterEx.DBUpdater()
mk = Analyzer.MarketDB()

codes_keys = list(mk.codes.keys())
codes_values = list(mk.codes.values())

sql_code_count = f"SELECT code, COUNT(*) as count FROM daily_price GROUP BY code"
code_count = pd.read_sql(sql_code_count, mk.conn)

sql_comp_list = f"SELECT * FROM company_info"
comp_list = pd.read_sql(sql_comp_list, mk.conn)

merge_df = pd.merge(comp_list, code_count, how='outer',
                    on='code').fillna(value=0)
merge_df.to_csv('code_count.csv', index=False, encoding='utf-8-sig')
# print(merge_df)

""" 어떤 code를 update할지 선정 """
stocks = list(merge_df[merge_df['count'] == 0]['code'])
# print(stocks)

# DB 수집할 주식 이름 혹은 코드 list
df = pd.DataFrame()

num = 0
for s in stocks:
    ''' If DB is not set, run the below code '''
    if s in codes_keys:
        code = s
    elif s in codes_values:
        idx = codes_values.index(s)
        code = codes_keys[idx]
    else:
        print(f"ValueError: Code({s}) doesn't exist.")
    temp_df = dbu.read_naver(code, mk.codes[code], 999999)
    dbu.replace_into_db(temp_df, num, code, mk.codes[code])
    num += 1
