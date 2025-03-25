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

find_creators = []
contents = ''''''

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


def chat_tab(tab_chat, nickname_text):
    Utils.delay(t=5)
    chat_flag = True
    while chat_flag:

        # index-module__sdkBox--RAScS

        # tab_chat.ele('@text()=No chat selected.')
        all = tab_chat.ele('@class=m4b-menu-item-children')
        print(all.text)
        match = re.search(r'\d+', all.text)  # 提取数字部分
        if match:
            num = int(match.group())
            if num >= 1000:
                # print('可以聊天了')
                chat_flag = False

                Utils.delay()

        submodule_layout_container_id = tab_chat.ele('@id=submodule_layout_container_id')
        # No_chat_selected = submodule_layout_container_id.child().child().children()[1].child().child().child().child().children()[1].child().child().child().child().children()[1]
        No_chat_selected = submodule_layout_container_id.child().child().children()[1].child().child().child().child().children()[1].child().child().children()
        print(len(No_chat_selected))

        # if No_chat_selected.text != 'No chat selected.':
        if len(No_chat_selected) >= 2:
            Utils.delay()
            chat_flag = False

            # workbench-container
            workbench_container = tab_chat.ele('@id=workbench-container')
            if workbench_container:
                workbench_nickname = workbench_container.child().children()[1].child().child().child().child().child().children()[1]
                print(workbench_nickname.text)

                # if workbench_nickname.text == nickname_text:
                #     chat_flag = False

                Utils.delay()

                product_lists = tab_chat.ele('@class=arco-tabs-header').children()[1].child().child().child().child()
                product_lists.click()


                Utils.delay()


                search_name_input = tab_chat.ele('@id=arco-tabs-0-panel-1').child().child().child().children()[1].child().child().child()
                search_name_input.input('vip')

                Utils.delay()

                search_name_button = tab_chat.ele('@id=arco-tabs-0-panel-1').child().child().child().children()[1].child().child().children()[2]
                search_name_button.click()

                Utils.delay()

                first_vip_goods_button = tab_chat.ele('@class=arco-tabs-content-inner').children()[1].child().child().children()[1].child().child().child().child().children()[1].child()
                # print('发送商品消息:', first_vip_goods_button.text)

                Utils.delay()

                textarea = tab_chat.ele('@id=im_sdk_chat_input').children()[1]
                # textarea.input(contents)

                Utils.delay()

                send_button = tab_chat.ele('@id=im_sdk_chat_input').children()[2].child().children()[1]
                # print('发送文本消息:', send_button)

                Utils.delay()

        Utils.delay()


def get_filter(tab):
    pass
    # filter_by_items = tab.ele('@id=submodule_layout_container_id').child().children()[1].child().child().child().children()[1].child().child().children()[1].child()
    # filter_by_items[0].click()

def set_filter():
    pass


def activate_tab():
    Utils.delay()
    # 连接到已打开的浏览器
    browser = Chromium()

    # 获取所有已打开的标签页
    tabs = browser.get_tabs()
    # print(tabs)
    # print(len(tabs))

    # 目标标题（请修改为你要找的标题）
    target_title = "TikTok Shop"

    # 查找符合标题的标签页
    for tab in tabs:
        # print('tab', tab)

        if target_title in tab.title:
            browser.activate_tab(tab.tab_id)  # 切换到该标签页
            # print(f"已切换到 {tab.title}")

            start_task(browser, tab)
            break
    else:
        print("未找到匹配的标签页")

def start_task(browser, tab):

    # **第一时间保存 Cookies**
    # tab.refresh()
    save_cookies(browser)  # 避免意外退出导致 cookies 丢失

    # 尝试点击 "Check it out" 按钮
    try:
        tab.ele('@text()=Check it out').click()
    except Exception:
        pass

    Utils.delay()

    count = 0
    while True:
        # if True:

        # 获取 class 为 'arco-table-body' 的元素
        table_body = tab.ele('@class=arco-table-body')
        if table_body:
            table = table_body.child('tag:table')
            tbody = table.children()[1] if len(table.children()) >= 2 else None

            if tbody:
                trs = tbody.children()
                # print('个数:', len(trs))
                for i in range(len(trs) // 2):
                    tr = trs[i * 2]
                    tds = tr.children()

                    if len(tds) > 1:
                        td = tds[0]
                        nickname = td.child().child().child().children()[1].child().child().child()
                        nickname_text = nickname.text
                        if nickname_text in find_creators:
                            pass
                        else:
                            print(nickname_text)
                            find_creators.append(nickname.text)

                            # 打开聊天对话框
                            if len(tds) > 6:
                                td = tds[6]
                                message_button = td.child().child().child().children()[1].child()
                                print(message_button)
                                message_button.click()

                                tabs = browser.get_tabs()

                                tab_chat = tabs[0]
                                chat_tab(tab_chat, nickname_text)

                                Utils.delay()

                                browser.close_tabs(tab_chat)
                                Utils.delay()

                count += 1
                # print(count)

                # 页面向下滚动 50 像素
                Utils.delay()

                ac.move_to(ele_or_loc=table_body, offset_y=count * 50).scroll(delta_y=50)



    # 保存最新 Cookies
    save_cookies(tab)

    print("Page Title:", tab.title)
    browser.quit()



import sys
from PySide6.QtWidgets import (QApplication)
from tiktokshop_widget import TiktokShopWidget


def main():
    # launch_with_cookies()
    activate_tab()

if __name__ == '__main__':
    # main()

    app = QApplication(sys.argv)

    widget = TiktokShopWidget()
    # 设置QWidget的固定大小
    widget.setFixedSize(650, 750)
    widget.show()

    sys.exit(app.exec())