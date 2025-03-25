from DrissionPage import Chromium, SessionPage
from DrissionPage.common import Actions
from DrissionPage.common import Settings
import time
import os
import re
from util import Utils


# 目标网址
URL = 'https://partner.us.tiktokshop.com/affiliate-cmp/creator?market=100'
COOKIES_FILE = 'cookies.txt'
CREATORS_FILE = 'processed_creators.txt'  # 保存已处理的 nickname

find_creators = []

class Core(object):

    def __init__(self):
        # 设置语言
        Settings.set_language('en')
        # 目标标题（请修改为你要找的标题）
        self.target_title = "TikTok Shop"
        # 总运行次数
        self.run_total_count = 0
        # 运行次数
        self.run_count = 0
        # 连接到已打开的浏览器
        self.browser = Chromium()
        # 加载已处理的 creators
        self.find_creators = self.load_processed_creators()

    def Set_run_total_count(self, count):
        """运行总次数"""
        self.run_total_count = count

    def Start(self):
        """开始任务"""
        self.activate_tab()

    def Stop(self):
        """停止任务"""
        pass

    def load_processed_creators(self):
        """从本地文件加载已处理的 nickname"""
        if not os.path.exists(CREATORS_FILE):
            return set()

        with open(CREATORS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f.readlines())

    def save_processed_creator(self, nickname):
        """保存新的 nickname 到本地文件"""
        with open(CREATORS_FILE, 'a', encoding='utf-8') as f:
            f.write(nickname + '\n')
        self.find_creators.add(nickname)

    def load_cookies(self):
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

    def save_cookies(self, browser):
        """从浏览器提取最新的 cookies 并保存到文件"""
        cookies = browser.cookies()  # 从浏览器获取 cookies
        if cookies:
            with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                f.write('; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]))
            print("Cookies saved successfully!")
        else:
            print("Failed to get cookies!")

    def activate_tab(self):
        # 获取所有已打开的标签页
        tabs = self.browser.get_tabs()

        # 查找符合标题的标签页
        for tab in tabs:
            if self.target_title in tab.title:
                self.browser.activate_tab(tab.tab_id)  # 切换到该标签页
                self.start_task(tab)
                break
        else:
            print("未找到匹配的标签页")

    def start_task(self, tab):
        ac = Actions(tab)

        # **第一时间保存 Cookies**
        self.save_cookies(self.browser)  # 避免意外退出导致 cookies 丢失

        Utils.delay()

        self.run_count = 0
        while True:
            # 获取 class 为 'arco-table-body' 的元素
            table_body = tab.ele('@class=arco-table-body')
            if table_body:
                table = table_body.child('tag:table')
                tbody = table.children()[1] if len(table.children()) >= 2 else None
                if tbody:
                    trs = tbody.children()
                    for i in range(len(trs) // 2):
                        tr = trs[i * 2]
                        tds = tr.children()

                        if len(tds) > 1:
                            td = tds[0]
                            nickname = td.child().child().child().children()[1].child().child().child()
                            nickname_text = nickname.text
                            if nickname_text in self.find_creators:
                                pass
                            else:
                                print(nickname_text)
                                # find_creators.append(nickname_text)
                                self.save_processed_creator(nickname_text) # 保存到本地文件

                                # 打开聊天对话框
                                if len(tds) > 6:
                                    td = tds[6]
                                    message_button = td.child().child().child().children()[1].child()
                                    message_button.click()

                                    tabs = self.browser.get_tabs()

                                    tab_chat = tabs[0]
                                    # chat_tab(tab_chat, nickname_text)

                                    Utils.delay(t=10)
                                    if self.target_title in tab_chat.title:
                                        pass
                                    else:
                                        self.browser.close_tabs(tab_chat)
                                        Utils.delay()

                    self.run_count += 1
                    # print(self.run_count)

                    # 页面向下滚动 50 像素
                    Utils.delay()

                    ac.move_to(ele_or_loc=table_body, offset_y=self.run_count * 50).scroll(delta_y=50)




        # 保存最新 Cookies
        self.save_cookies(self.browser)


