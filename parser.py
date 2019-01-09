from matplotlib.cbook import flatten
import pandas as pd


def parser_row_val(df, row_no, item_no):
    '''
    解析每一行 row values的資料 將交易量做單位換算為公斤後回傳 allrow

    df: pd.read_html(table_source)
    row_no: html table's row number
    item_no:產品項目

    allrow : list data [[]]
    '''
    # 單位轉換
    def unit_transform(arg):
        if (arg[0] == "0") or (arg[0] == 'No Quantity'):
            return 0.0
        elif arg[1] == "Tons":
            return float(arg[0]) * 907.18474
        elif arg[1] == "Pounds":
            return float(arg[0]) * 0.45359237
        elif arg[1] == "Hundreds units":
            return float(arg[0]) * 100
        elif arg[1] == "Thousands units":
            return float(arg[0]) * 1000
        elif arg[1] in ["Dozens", "Heads"]:
            return 0.0
        elif arg[1] in ["Kilograms", 'Units', 'Unit', 'Mixed']:
            return float(arg[0])

    country_a = "world"
    #     row_no = 3
    country_b = df.loc[row_no][1]
    row_val = df.loc[row_no][2:].tolist()

    date_list = df.loc[0][2:].dropna().tolist()
    if "in" in date_list[0]:
        date_list = [x.split("in ")[1] for x in date_list]  # 只保留 date
    date_list = list(flatten(zip(date_list, date_list)))  # 複製一份 date

    # parser row_val value
    allrow = []
    for i in range(0, len(row_val), 2):
        arg = (row_val[i], row_val[i + 1])
        v = unit_transform(arg)
        row = [country_a, country_b, item_no, date_list[i], v]
        allrow.append(row)
    return allrow


def remake(df, item_no, value_header):
    '''
    整理 table_source df 並回傳 DataFrame

    df : pd.read_html(table_source)
    item_no : str  產品項目, ex: "020711", "020712" , "020714", "020742"
    value_header :str 貿易資訊, ex: "ex_qty","im_qty","ex_val","im_val"
    '''
    columns = ['country_a', 'country_b', 'item_no', 'date', value_header]

    records = []
    for row_no in range(2, len(df)):  # 資料從第三行開始
        allrow = parser_row_val(df, row_no, item_no)
        for row in allrow:
            records.append(row)

    df2 = pd.DataFrame.from_records(records, columns=columns)
    return df2


if __name__ == "__main__":
    df = pd.read_pickle('./pickle/test.pickle')
    df2 = remake(df, "020712", "im_qty")
    print(df2)
