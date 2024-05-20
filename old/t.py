import requests
from bs4 import BeautifulSoup

url = "https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=46757"

# 發送GET請求
response = requests.get(url)

# 檢查響應狀態碼
if response.status_code == 200:
    response_j = response.json()
    print(response_j)
    # 將HTML內容轉換為BeautifulSoup物件
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 這裡可以繼續使用BeautifulSoup來提取你需要的資料
    # 例如，找到所有的表格:
    tables = soup.find_all("table")
    
    # 遍歷每個表格並提取資料
    for table in tables:
        # 處理表格內容，這裡只是示範
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            for column in columns:
                print(column.text)
else:
    print("Failed to retrieve data from the URL.")
