from PySide6.QtWidgets import (
    QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QApplication,
    QRadioButton, QTimeEdit
)
from PySide6.QtGui import QPalette, QColor, QIntValidator
from PySide6.QtCore import QThread, Signal, QSettings, QTimer, QTime
import sys
from core import Core

TITLE = '辅助工具'
DEFAULT_SEARCH_CONTENT = 'vip'
DEFAULT_SEND_CONTENT = '''Free sanples!!!!
Hello! This is Tik Tok TOP partner. We sincerely invite you to participate in our spring promotion cooperation plan!
This event is unprecedented in intensity, and you will receive thousands of popular samples (covering clothing, beauty, home and other popular categories) for free application;
Exclusive product selection link: 100 selected free products (attached), one click to add showcase, and enjoy profit sharing upon sale;
Operation process:
① Click on the product link → ② Add to showcase → ③ Apply for samples in the background
Top selling bloggers during the event can also unlock mysterious rewards! Looking forward to a win-win spring business opportunity with you! Looking forward to receiving your reply
'''

class WorkerThread(QThread):
    finished_signal = Signal()  # 任务完成信号
    error_signal = Signal(str)  # 任务出错信号

    def __init__(self, core, run_count, keyword, contents):
        super().__init__()
        self.core = core
        self.run_count = run_count
        self.keyword = keyword
        self.contents = contents

    def run(self):
        """ 在子线程中执行核心任务 """
        print('开始任务')
        try:
            self.core.Set_run_total_count(self.run_count)
            self.core.Set_search_keyword(self.keyword)
            self.core.Set_send_content(self.contents)
            self.core.Start()
            self.finished_signal.emit()  # 任务完成后，发送信号
        except Exception as e:
            self.error_signal.emit(str(e))  # 任务出错，发送错误信号

class TiktokShopWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.settings = QSettings("MyCompany", "TiktokTool")  # 定义存储位置
        self.init_ui()
        self.load_settings()  # 载入上次保存的数据

        self.core = Core()
        self.worker_thread = None  # 线程对象
        self.timer = QTimer(self)

    def init_ui(self):
        # 运行次数输入框 (只能输入数字)
        self.run_count_input = QLineEdit(self)
        self.run_count_input.setPlaceholderText("输入运行次数")
        self.run_count_input.setValidator(QIntValidator(1, 10000, self))  # 仅允许 1-10000 的数字

        self.run_interval_time = QLineEdit(self)
        self.run_interval_time.setPlaceholderText("输入间隔时间")
        self.run_interval_time.setValidator(QIntValidator(1, 10000, self))  # 仅允许 1-10000 的数字

        # 搜索内容输入框
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("输入搜索内容")

        # 发送内容 (多行文本输入框)
        self.message_input = QTextEdit(self)
        self.message_input.setPlaceholderText("输入发送的内容")

        # 立即执行 & 定时执行 选项
        self.immediate_radio = QRadioButton("立即执行", self)
        self.schedule_radio = QRadioButton("定时执行", self)
        self.immediate_radio.setChecked(True)

        # 定时启动时间选择
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setEnabled(False)

        # 按钮
        self.start_button = QPushButton("开始", self)
        self.stop_button = QPushButton("停止", self)

        # 状态标签
        self.status_label = QLabel("状态: 未运行", self)
        self.set_status_color("gray")  # 初始状态为灰色

        # 日志组件
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        # 绑定按钮事件
        self.start_button.clicked.connect(self.start_task)
        self.stop_button.clicked.connect(self.stop_task)
        self.immediate_radio.toggled.connect(self.toggle_time_edit)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(QLabel("运行次数:"))
        layout.addWidget(self.run_count_input)

        layout.addWidget(QLabel("间隔时间:"))
        layout.addWidget(self.run_interval_time)

        layout.addWidget(QLabel("搜索内容:"))
        layout.addWidget(self.search_input)

        layout.addWidget(QLabel("发送内容 (多行):"))
        layout.addWidget(self.message_input)

        # 添加执行模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.immediate_radio)
        mode_layout.addWidget(self.schedule_radio)
        layout.addLayout(mode_layout)

        # 定时启动时间
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("定时启动时间:"))
        time_layout.addWidget(self.time_edit)
        layout.addLayout(time_layout)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        layout.addLayout(btn_layout)


        layout.addWidget(self.status_label)

        layout.addWidget(self.log_output)


        self.setLayout(layout)

        self.start_button.setEnabled(True)  # 开始按钮默认可点击
        self.stop_button.setEnabled(False)  # 停止按钮默认不可点击

    def toggle_time_edit(self):
        """ 选择 '定时执行' 时启用时间选择框 """
        self.time_edit.setEnabled(self.schedule_radio.isChecked())

    def start_task(self):
        """ 开始任务 """
        run_count = self.run_count_input.text()
        search_content = self.search_input.text()
        message_content = self.message_input.toPlainText()  # 获取多行文本内容

        if not run_count.isdigit():
            self.status_label.setText("状态: 运行次数必须是数字")
            self.set_status_color("red")
            return

        # self.status_label.setText(f"状态: 运行中 ({run_count} 次)")
        # self.set_status_color("green")
        # print(f"开始运行: {run_count} 次，搜索内容: {search_content}\n发送内容:\n{message_content}")
        #
        # # 禁用开始按钮，防止重复点击
        # self.start_button.setEnabled(False)
        # self.stop_button.setEnabled(True)
        #
        # # 启动子线程
        # self.worker_thread = WorkerThread(self.core, int(run_count))
        # self.worker_thread.finished_signal.connect(self.on_task_finished)
        # self.worker_thread.error_signal.connect(self.on_task_error)
        # self.worker_thread.start()  # 启动子线程

        if self.schedule_radio.isChecked():  # 如果是定时执行
            self.schedule_task()
        else:
            self.execute_task()

    def schedule_task(self):
        """ 定时执行任务 """
        target_time = self.time_edit.time()
        current_time = QTime.currentTime()

        # 计算启动时间
        interval_ms = current_time.msecsTo(target_time)

        if interval_ms <= 0:
            self.status_label.setText("状态: 时间无效，请选择未来时间")
            self.set_status_color("red")
            return

        self.status_label.setText(f"状态: 任务将在 {target_time.toString()} 启动")
        self.set_status_color("orange")

        # 设置定时器
        self.timer.singleShot(interval_ms, self.execute_task)

        # 禁用开始按钮，避免重复点击
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def execute_task(self):
        """ 立即执行任务 """
        run_count = int(self.run_count_input.text())
        search_content = self.search_input.text()
        message_content = self.message_input.toPlainText()

        self.status_label.setText(f"状态: 运行中 ({run_count} 次)")
        self.set_status_color("green")

        print(f"开始运行: {run_count} 次，搜索内容: {search_content}\n发送内容:\n{message_content}")

        # 禁用按钮
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # 启动子线程
        self.worker_thread = WorkerThread(self.core, run_count, search_content, message_content)
        self.worker_thread.finished_signal.connect(self.on_task_finished)
        self.worker_thread.error_signal.connect(self.on_task_error)
        self.worker_thread.start()

    def stop_task(self):
        """ 停止任务 """
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()  # 强制终止 (不推荐)
            self.worker_thread.wait()

        self.status_label.setText("状态: 已停止")
        self.set_status_color("red")

        # 恢复按钮状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)



    def on_task_finished(self):
        """ 任务完成后更新 UI """
        self.status_label.setText("状态: 任务完成")
        self.set_status_color("blue")

        # 任务完成后恢复按钮状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_task_error(self, error_message):
        """ 任务出错时更新 UI """
        self.status_label.setText(f"状态: 错误 - {error_message}")
        self.set_status_color("red")

        # 任务出错后恢复按钮状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def set_status_color(self, color):
        """ 设置状态标签的颜色 """
        palette = self.status_label.palette()
        palette.setColor(QPalette.WindowText, QColor(color))
        self.status_label.setPalette(palette)

    def closeEvent(self, event):
        """ 监听窗口关闭事件，保存输入框数据 """
        self.save_settings()
        event.accept()

    def save_settings(self):
        """ 保存用户输入的设置 """
        self.settings.setValue("run_count", self.run_count_input.text())
        self.settings.setValue("search_content", self.search_input.text())
        self.settings.setValue("message_content", self.message_input.toPlainText())
        print("设置已保存")

    def load_settings(self):
        """ 载入上次保存的设置 """
        self.run_count_input.setText(self.settings.value("run_count", "10"))
        self.search_input.setText(self.settings.value("search_content", DEFAULT_SEARCH_CONTENT))
        self.message_input.setText(self.settings.value("message_content", DEFAULT_SEND_CONTENT))
        print("设置已加载")


# 运行界面
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TiktokShopWidget()
    window.show()
    sys.exit(app.exec())
