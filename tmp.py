from DrissionPage import Chromium, SessionPage
from DrissionPage.common import Actions
from DrissionPage.common import Settings
import time
import os
import re
from util import Utils

# 设置语言
Settings.set_language('en')

# 目标网址
URL = 'https://partner.us.tiktokshop.com/affiliate-cmp/creator?market=100'
COOKIES_FILE = 'cookies.txt'

def load_cookies():
    """从文件加载 cookies"""
    if not os.path.exists(COOKIES_FILE):
        return []

    cookies = []
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        for line in f.read().strip().split('; '):
            if '=' in line:
                name, value = line.split('=', 1)
                cookies.append({'name': name, 'value': value, 'domain': '.tiktokshop.com', 'path': '/'})
    return cookies


def save_cookies(browser):
    """从浏览器提取最新的 cookies 并保存到文件"""
    cookies = browser.cookies()  # 从浏览器获取 cookies
    if cookies:
        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            f.write('; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]))
        print("Cookies saved successfully!")
    else:
        print("Failed to get cookies!")

def launch_with_cookies():
    """使用 Chromium 启动并自动化操作"""
    browser = Chromium()
    tab = browser.new_tab()
    ac = Actions(tab)

    # 加载最新 Cookies
    cookies = load_cookies()
    if cookies:
        tab.set.cookies(cookies)

    print('访问页面')
    tab.get(URL)

    time.sleep(3)

    # **第一时间保存 Cookies**
    tab.refresh()
    save_cookies(browser)  # 避免意外退出导致 cookies 丢失


    # 尝试点击 "Check it out" 按钮
    try:
        tab.ele('@text()=Check it out').click()
    except Exception:
        pass

    print('筛选')
    time.sleep(5)
    print('邀请')

    # get_filter(tab)

    time.sleep(3000000)

    while True:
        print('')

    # count = 0
    # while True:
    # # if True:
    #
    #     # 获取 class 为 'arco-table-body' 的元素
    #     table_body = tab.ele('@class=arco-table-body')
    #     if table_body:
    #         table = table_body.child('tag:table')
    #         tbody = table.children()[1] if len(table.children()) >= 2 else None
    #
    #         if tbody:
    #             trs = tbody.children()
    #             print('个数:', len(trs))
    #             for i in range(len(trs) // 2):
    #                 tr = trs[i * 2]
    #                 tds = tr.children()
    #
    #                 if len(tds) > 1:
    #                     td = tds[0]
    #                     nickname = td.child().child().child().children()[1].child().child().child()
    #                     nickname_text = nickname.text
    #                     if nickname_text in find_creators:
    #                         pass
    #                     else:
    #                         print(nickname_text)
    #                         find_creators.append(nickname.text)
    #
    #
    #                         # 打开聊天对话框
    #                         if len(tds) > 6:
    #                             td = tds[6]
    #                             message_button = td.child().child().child().children()[1].child()
    #                             message_button.click()
    #
    #
    #                             tabs = browser.get_tabs()
    #
    #
    #                             tab_chat = tabs[0]
    #                             chat_tab(tab_chat)
    #
    #
    #
    #                             time.sleep(30)
    #
    #
    #                             browser.close_tabs(tab_chat)
    #                             time.sleep(3)
    #
    #             count += 1
    #             print(count)
    #
    #             # 页面向下滚动 50 像素
    #             time.sleep(3)
    #             ac.move_to(ele_or_loc=table_body, offset_y=count * 50).scroll(delta_y=50)



        # tab.refresh()
        # time.sleep(5)



    # 保存最新 Cookies
    save_cookies(tab)

    print("Page Title:", tab.title)
    browser.quit()

if __name__ == '__main__':
    launch_with_cookies()