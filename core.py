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
        # 间隔时间
        self.run_interval_time = 0
        # 搜索的关键字
        self.search_keyword = ''
        # 发送的内容
        self.send_content = ''

        # 运行次数
        self.run_count = 0
        # 连接到已打开的浏览器
        self.browser = Chromium()
        # 加载已处理的 creators
        self.find_creators = self.load_processed_creators()

    def Set_run_total_count(self, count):
        """运行总次数"""
        self.run_total_count = count

    def Set_run_interval_time(self, interval_time):
        self.run_interval_time = interval_time

    def Set_search_keyword(self, search_keyword):
        """搜索的关键字"""
        self.search_keyword = search_keyword

    def Set_send_content(self, send_content):
        """发送的内容"""
        self.send_content = send_content

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
                                # self.save_processed_creator(nickname_text) # 保存到本地文件

                                # 打开聊天对话框
                                if len(tds) > 6:
                                    td = tds[6]
                                    print('打开私聊页面')
                                    message_button = td.child().child().child().children()[1].child()
                                    message_button.click(by_js=None, timeout=60)
                                    print('打开私聊页面 over')

                                    tabs = self.browser.get_tabs()

                                    tab_chat = tabs[0]
                                    self.chat_tab(tab_chat, nickname_text)

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

            # 任务间隔时长
            Utils.delay(t=self.run_interval_time)




        # 保存最新 Cookies
        self.save_cookies(self.browser)


    def chat_tab(self, tab_chat, nickname_text):
        Utils.delay(t=5)
        chat_flag = True
        while chat_flag:

            # # index-module__sdkBox--RAScS
            #
            # # tab_chat.ele('@text()=No chat selected.')
            # all = tab_chat.ele('@class=m4b-menu-item-children')
            # # print(all.text)
            # match = re.search(r'\d+', all.text)  # 提取数字部分
            # if match:
            #     num = int(match.group())
            #     if num >= 1000:
            #         # print('可以聊天了')
            #         chat_flag = False
            #
            #         Utils.delay()

            submodule_layout_container_id = tab_chat.ele('@id=submodule_layout_container_id')
            # No_chat_selected = submodule_layout_container_id.child().child().children()[1].child().child().child().child().children()[1].child().child().child().child().children()[1]
            No_chat_selected = submodule_layout_container_id.child().child().children()[1].child().child().child().child().children()[
                1].child().child().children()
            # print(len(No_chat_selected))

            # if No_chat_selected.text != 'No chat selected.':
            if len(No_chat_selected) >= 2:
                Utils.delay(t=5)
                chat_flag = False

                # workbench-container
                workbench_container = tab_chat.ele('@id=workbench-container')
                print('workbench_container=', workbench_container)
                if workbench_container:
                    # workbench_nickname = \
                    # workbench_container.child().children()[1].child().child().child().child().child().children()[1]
                    # print(workbench_nickname.text)

                    # if workbench_nickname.text == nickname_text:
                    #     chat_flag = False

                    Utils.delay()

                    print('切换-product_lists')
                    product_lists = tab_chat.ele('@id=workbench-container').child().child().child().child().child().children()[
                        1].child().child().child().child()
                    print("product_lists", product_lists)
                    print("product_lists", product_lists.text)
                    if product_lists:
                        print('悬浮')
                        product_lists.hover()
                        print('尝试点击元素...')
                        try:
                            product_lists.click(by_js=None, timeout=60)
                            print("点击成功！")
                        except Exception as e:
                            print(f"普通点击失败: {e}")
                            print("尝试使用 JavaScript 点击...")

                            try:
                                tab_chat.run_js("arguments[0].click();", product_lists)
                                print("JavaScript 点击成功！")
                            except Exception as e2:
                                print(f"JavaScript 点击失败: {e2}")
                                print("尝试模拟鼠标事件...")

                                try:
                                    tab_chat.run_js("""
                                            arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
                                            arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
                                            arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));
                                        """, product_lists)
                                    print("模拟鼠标事件点击成功！")
                                except Exception as e3:
                                    print(f"模拟鼠标事件失败: {e3}")
                                    print("尝试前置窗口并重新点击...")

                                    try:
                                        tab_chat.set_window_state('maximized')  # 最大化窗口
                                        time.sleep(0.5)
                                        tab_chat.set_window_state('normal')  # 还原窗口
                                        product_lists.click()
                                        print("窗口前置后点击成功！")
                                    except Exception as e4:
                                        print(f"所有点击方式均失败: {e4}")

                        # tab_chat.run_js("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));",
                        #                 product_lists)
                        # tab_chat.run_js("arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));",
                        #                 product_lists)
                        # tab_chat.run_js("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));",
                        #                 product_lists)

                    # if product_lists:
                    #     tab_chat.run_js('arguments[0].click();', product_lists)

                    Utils.delay()

                    search_container = tab_chat.ele('@id=workbench-container').child().children()[1].child().children()[1].child()
                    if search_container:

                        print('输入-搜索关键字')


                        search_name_input = tab_chat.ele('@id=workbench-container').child().children()[1].child().children()[1].child().child().child().children()[
                            1].child().child().child()
                        if search_name_input:
                            search_name_input.input(self.search_keyword)

                            Utils.delay()

                            search_name_button = tab_chat.ele('@id=workbench-container').child().children()[1].child().children()[1].child().child().child().children()[
                                1].child().child().children()[2]
                            if search_name_button:
                                search_name_button.click(by_js=None, timeout=60)

                            Utils.delay(t=5)

                            vip_search_results = tab_chat.ele('@class=arco-tabs-content-inner').children()[1].child().child().children()[
                                1].child().child().children()

                            if len(vip_search_results) > 2:
                                first_vip_goods_button = tab_chat.ele('@class=arco-tabs-content-inner').children()[1].child().child().children()[
                                    1].child().child().child().child().children()[1].child()
                                if first_vip_goods_button:
                                    first_vip_goods_button.click(by_js=None, timeout=60)
                                    # print('发送商品消息:', first_vip_goods_button.text)

                    Utils.delay()

                    textarea = tab_chat.ele('@id=im_sdk_chat_input').children()[1]
                    textarea.input(self.send_content)
                    # print('发送内容:' + self.send_content)
                    print('发送')
                    self.save_processed_creator(nickname_text)  # 保存到本地文件

                    Utils.delay()

                    send_button = tab_chat.ele('@id=im_sdk_chat_input').children()[2].child().children()[1]
                    if send_button:
                        send_button.click(by_js=None, timeout=60)
                    # print('发送文本消息:', send_button)

                    Utils.delay()

            Utils.delay()

