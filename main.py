import sys
from PySide6.QtWidgets import (QApplication)
from tiktokshop_widget import TiktokShopWidget


def main():
    app = QApplication(sys.argv)

    widget = TiktokShopWidget()
    # 设置QWidget的固定大小
    widget.setFixedSize(650, 750)
    widget.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

