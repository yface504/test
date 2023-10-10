from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup

# 将字符串"20230901"转换为日期格式
date_str = "20230801"
new_date = datetime.strptime(date_str, "%Y%m%d")

# 设置为该月的最后一天
last_day = datetime(new_date.year, new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])

# 构建 URL
wocha = "https://chl.cn/?" + str(new_date.year) + "-" + str(new_date.month) + "-" + str(last_day.day)

# 发送HTTP请求并获取页面内容
response = requests.get(wocha)
response.encoding = 'utf-8' #改變編碼解決亂碼問題

# 检查请求是否成功
if response.status_code == 200:
    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到第二个表格元素
    tables = soup.find_all('table')
    target_table = tables[1]  # 第二个表格

    # 初始化关键字位置的变量
    keyword_position = None

    # 在整个表格中搜索关键字
    for i, td in enumerate(target_table.find_all('td')):
        # 如果关键字"100日元/人民币"在<td>元素中
        if "美元/人民币" in td.get_text():
            keyword_position = i  # 记录关键字位置
            break  # 找到后停止寻找

    if keyword_position is not None:
        print("关键字位置是表格的第", keyword_position, "个td")
    else:
        print("未找到关键字")

    #獲取100日元該行的下1格數值
    td_elements = tables[1].find_all('td')
    target_td = td_elements[i+1]  # 这里选择了第十个<td>元素
    target_value = target_td.get_text()
    numeric_value = float(target_value) / 100
    print("目标数值:", numeric_value)

else:
    print("HTTP请求失败，状态码:", response.status_code)
