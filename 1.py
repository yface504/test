from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup

# 获取用户输入
user_input = input("请输入 a~g: ")

# 将字符串"20230901"转换为日期格式
date_str = "20230801"
new_date = datetime.strptime(date_str, "%Y%m%d")

# 设置为该月的最后一天
last_day = datetime(new_date.year, new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])

# 构建 URL
wocha = "https://chl.cn/?" + str(new_date.year) + "-" + str(new_date.month) + "-" + str(last_day.day)

# 发送HTTP请求并获取页面内容
response = requests.get(wocha)
response.encoding = 'utf-8'  # 改变编码解决乱码问题

# 检查请求是否成功
if response.status_code == 200:
    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到对应的表格
    table_index = None
    keyword = None

    if user_input == 'A':
        table_index = 0
        keyword = "新台币"
    elif user_input == 'B':
        table_index = 1
        keyword = "100日元/人民币"
    elif user_input == 'C':
        table_index = 1
        keyword = "美元/人民币"
    elif user_input == 'D':
        table_index = 0
        keyword = "日元"
    elif user_input == 'E':
        table_index = 0
        keyword = "日元"
    elif user_input == 'F':
        table_index = 0
        keyword = "美元"
    elif user_input == 'G':
        table_index = 0
        keyword = "美元"

    if table_index is not None and keyword is not None:
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
            if user_input == 'A':
                result = (float(td_elements[keyword_position + 2].get_text()) + float(td_elements[keyword_position + 4].get_text())) / 200
            elif user_input == 'B':
                result = float(td_elements[keyword_position + 1].get_text()) / 100
            elif user_input == 'C':
                result = float(td_elements[keyword_position + 1].get_text())
            elif user_input == 'D':
                result = float(td_elements[keyword_position + 1].get_text()) / 100
            elif user_input == 'E':
                result = float(td_elements[keyword_position + 4].get_text()) / 100
            elif user_input == 'F':
                result = float(td_elements[keyword_position + 1].get_text()) / 100
            elif user_input == 'G':
                result = float(td_elements[keyword_position + 4].get_text()) / 100

            # 格式化结果为小数点后4位
            formatted_result = "{:.4f}".format(result)
            print("目标数值:", formatted_result)

        else:
            print("未找到关键字")

    else:
        print("无效的输入")

else:
    print("HTTP请求失败，状态码:", response.status_code)