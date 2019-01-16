from functools import reduce
import spider
from parser import remake
from toJson import toJson
import pandas as pd
import json
from setlog import setlog
logging = setlog()

__version__ = '1.0'


'''
Run
1.爬蟲 2.解析 3.轉成json
'''

ac = "ponggung1986@gmail.com"
pw = "W8Ce5wW5z2qMs2K"
pdir="./pickle/"

# Records = ["Exports", "Imports"]
# Indicators = ["Values", "Quantities"]
Records = Indicators = [1, 2]
recs = ["ex", "im"]
inds = ["val", "qty"]

# 產品項目
products = ["020711", "020712", "020714", "040700"]
options = [[3, 10, 10], [4], [5], [1, 5, 12, 10]]

s = spider.TradeSpider()
s.setDriver()
s.login(ac, pw)
s.setTimePage()

p = 0
for index, o in enumerate(options):
    for n in o:
        s.selectProducts(n)
    for r in Records:
        for i in Indicators:

            # spider
            s.setRecords(r)
            s.setIndicators(i)
            s.save(pdir + str(p))

            # parser
            df = pd.read_pickle(pdir + str(p) + '.pickle')
            value_header = "{}_{}".format(recs[r-1], inds[i-1])
            item = products[index]

            re_df = remake(df, item, value_header)
            re_df.to_pickle(pdir + str(p) + '.pickle')
            p += 1

s.close()
# merge & concat

n = 16  # 4 x 2 x 2
df_all = pd.DataFrame()

# 每四個 df merge一次，merge的結果concat到 df_all
for x in range(0, n, 4):
    data_frames = [
        pd.read_pickle(pdir + str(i) + '.pickle') for i in range(x, x + 4)
    ]

    df_merge = reduce(lambda left, right: pd.merge(left, right, on=["country_a", "country_b", "date", "item_no"],
                                                   how='outer'), data_frames).fillna(0.0) # 缺值紀錄設為 0.0
    df_all = pd.concat([df_all, df_merge])

# 將交易紀錄轉換為 pandas DataFrame
df_all.to_pickle(pdir + "df_all.pickle")

# toJson
jsonData = toJson(df_all)
with open("map_result.json", "w") as file:
    file.write(json.dumps(jsonData, ensure_ascii=False, indent=2))
