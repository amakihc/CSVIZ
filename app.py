# app.py

from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_layout import UILayout
import sys

class App(QMainWindow):
    """
    アプリケーションのメインウィンドウクラス
    """
    def __init__(self):
        super().__init__()
        # UILayoutクラスのインスタンスを作成
        self.ui = UILayout()
        # メインウィンドウにUIを設定
        self.setCentralWidget(self.ui)
        self.setGeometry(100, 100, 1200, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())