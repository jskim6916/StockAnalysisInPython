import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer
from Investar import DBUpdaterEx

dbu = DBUpdaterEx.DBUpdater()
mk = Analyzer.MarketDB()

codes_keys = list(mk.codes.keys())
codes_values = list(mk.codes.values())

stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()

num = 0
for s in stocks:

    # ''' If DB is not set, run the below code '''
    # if s in codes_keys:
    #     pass
    # elif s in codes_values:
    #     idx = codes_values.index(s)
    #     code = codes_keys[idx]
    # else:
    #     print(f"ValueError: Code({s}) doesn't exist.")
    # temp_df = dbu.read_naver(code, mk.codes[code], 999999)
    # dbu.replace_into_db(temp_df, num, code, mk.codes[code])
    # num += 1

    df[s] = mk.get_daily_price(s, '2016-01-04', '2018-04-27')['close']

daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252

port_ret = []
port_risk = []
port_weights = []

for _ in range(20000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Risk', 'Returns'] + [s for s in stocks]]

df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
