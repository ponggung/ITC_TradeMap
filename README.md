# ITC_TradeMap

- 目標網站: https://www.trademap.org/Country_SelProduct_TS.aspx   
- 網站敘述: ITC Trade Map 資料庫, 包含世界各國的農產品進出口紀錄   
- 爬蟲要求: 下載特定品項的每月進出口值、量  

(1) Products = [
"020711 - Fresh or chilled fowls of the species Gallus domesticus, not cut in pieces" "020712 - Frozen fowls of the species Gallus domesticus, not cut in pieces" "020714 - Frozen cuts and edible offal of fowls of the species Gallus domesticus" "040700 - Birds' eggs, in shell, fresh, preserved or cooked"]
(2) Countries = "World"
(3) Records = ["Exports", "Imports"]
(4) Timeseries = "Monthly time series"
(5) Indicators = ["Values", "Quantities"]
(6) Time Period (number of columns) = "20 per page"
(7) Rows per page = "300 per page"
(8) ...其餘為網站預設值

![web](img/web.png)  
![df](img/df.png)


## 主程式

Step | Work | Code
---|:---:|---
1|爬蟲|spider.py
2|解析 HTML|parser.py.py
3|DataFrame 格式轉換成json| toJson.py


## Install
```
sudo pip install -r requirement.txt
```

## Driver version
```
firefox 64.0  
geckodriver v0.23.0  
https://github.com/mozilla/geckodriver/releases
```

## Quick test
```
python spider.py
python parser.py
python toJson.py
check.ipynb
```

## Run
```
python run.py
```
![log](img/log.png)

## Output
```
df_all.pickle
map_result.json
```
![json](img/json.png)

