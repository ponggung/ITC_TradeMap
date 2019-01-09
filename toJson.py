import pandas as pd
from collections import defaultdict
import json

folder = "./sample-data/"


def toJson(df):
    '''
    input: ITC Trade Map HTML,將交易紀錄解析後的 pandas DataFrame
    output: JSON 格式資料, 
    '''

    # init
    output = {"filters": {"產品項目": [], "年份": [], "貿易資訊": []}, "values": {}}
    # 貿易資訊
    output["filters"]["貿易資訊"] = [["ex_qty", "出口量(KG)"], ["im_qty", "進口量(KG)"],
                                 ["ex_val", "出口值(US dollar)"],
                                 ["im_val", "進口值(US dollar)"]]

    # Get mapping
    with open(folder + "ch_country_mapping.json", "r") as file:
        country_map = json.load(file)
    with open(folder + "hs_cname_mapping.json", "r") as file:
        cname_map = json.load(file)

    # 產品項目
    product_item = []
    item_no_list = df["item_no"].unique()
    for item_no in item_no_list:
        product_item.append([item_no, cname_map[item_no]])
    output["filters"]["產品項目"] = product_item

    # 年份
    years = list(df["date"].unique())
    if "-" in str(years[0]):
        years = [x.split("-")[0] for x in years]
    # 日期限定 2010 年至 2015 年
    years = [int(x) for x in years if int(x) >= 2010 and int(x) <= 2015]
    years.sort()
    output["filters"]["年份"] = years

    # Values
    values_dict = {}

    df_sum = df.groupby(["item_no", "date", "country_b"]).sum()

    im_ex = ["ex_val", "im_val", "ex_qty", "im_qty"]
    key = ""
    for _im_ex in im_ex:
        for index, row in df_sum.iterrows():
            key_p = "{}-{}-{}".format(index[0], index[1], _im_ex)
            country = country_map[index[2]]
            if key != key_p:
                country_vals = {}  # 新的一組key，country_vals 歸零
                key = key_p
            if row[_im_ex] > 0:
                country_vals[country] = int(row[_im_ex])
                values_dict[key] = country_vals
    output["values"] = values_dict
    return output


if __name__ == "__main__":
    # Get pickle
    df = pd.read_pickle(folder + 'df_1015_sample.pickle')
    # df = pd.read_pickle('df_sample.pickle')

    jsonData = toJson(df)
    print(jsonData)
    with open("map_result.json", "w") as file:
        file.write(json.dumps(jsonData, ensure_ascii=False, indent=2))
