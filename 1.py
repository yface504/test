from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup

# 字典 - 匯率方式映射到第幾張表格、關鍵字、公式
area_rate = area + ',' + exchange_rate_method
area_rate_map = {
    '台湾,中间价': (0, "新台币", lambda td_elements, keyword_position: (float(td_elements[keyword_position + 2].get_text()) + float(td_elements[keyword_position + 4].get_text())) / 200),
    '日本,中间价': (1, "100日元/人民币", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
    '美国,中间价': (1, "美元/人民币", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text())),
    '日本,汇款买入价': (0, "日元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
    '日本,汇款卖出价': (0, "日元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 4].get_text()) / 100),
    '美国,汇款买入价': (0, "美元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
    '美国,汇款卖出价': (0, "美元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 4].get_text()) / 100)
}

# 將titleDate轉換為日期格式，設置為該月的最後一天
new_date = datetime.strptime(titleDate+ '01', "%Y%m%d")
last_day = datetime(new_date.year, new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])

# 构建 URL
wocha = "https://chl.cn/?" + str(new_date.year) + "-" + str(new_date.month) + "-" + str(last_day.day)

# 发送HTTP请求并获取页面内容
response = requests.get(wocha)
response.encoding = 'utf-8'  #改變頁面內容的編碼

# 检查请求是否成功
if response.status_code == 200:
    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取用户输入对应的映射数据
    table_index, keyword, formula = area_rate_map.get(area_rate, (None, None, None))

    if table_index is not None and keyword is not None and formula is not None:
        # 找到对应的表格元素
        tables = soup.find_all('table')
        target_table = tables[table_index]

        # 初始化关键字位置的变量
        keyword_position = None

        # 在整个表格中搜索关键字
        for i, td in enumerate(target_table.find_all('td')):
            # 如果关键字在<td>元素中
            if keyword in td.get_text():
                keyword_position = i  # 记录关键字位置
                break  # 找到后停止寻找

        if keyword_position is not None:
            print("关键字位置是表格的第", keyword_position, "个td")

            # 获取相应的数值并应用公式
            td_elements = target_table.find_all('td')
            result = formula(td_elements, keyword_position)

            # 外匯匯率小數點後6位
            FxRate = "{:.6f}".format(result)
            print("目標匯率:", FxRate)

            # 外匯匯率時間
            h1s = soup.find_all('h1')
            banktime = h1s[0].get_text()
            print("匯率時間:", banktime)
        else:
            print("未找到關鍵字")
    else:
        print("匯率方式為無，或台幣只支援中間價的匯率方式")
        FxRate =1
else:
    print("HTTP請求失敗，狀態碼:", response.status_code)