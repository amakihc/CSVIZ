# gui_layout.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
import pyqtgraph as pg

class UILayout(QWidget):
    """
    アプリケーションのUIレイアウトを構築するクラス
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Data Viewer")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # UIコンポーネントを初期化
        self.create_widgets()
        # レイアウトにウィジェットを追加
        self.add_widgets_to_layout()

    def create_widgets(self):
        """
        UIで使用するウィジェットを作成
        """
        # ボタンとラベル
        self.browse_button = QPushButton("CSVファイルを選択")
        self.file_path_label = QLabel("ファイルが選択されていません")

        # グラフウィジェット
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.time_series_plot = pg.PlotWidget()
        self.time_series_plot.setTitle("時系列プロット")
        self.time_series_plot.setLabel('bottom', '時間')
        self.time_series_plot.setLabel('left', '振幅')

        self.psd_plot = pg.PlotWidget()
        self.psd_plot.setTitle("パワースペクトル密度 (PSD)")
        self.psd_plot.setLabel('bottom', '周波数 (Hz)')
        self.psd_plot.setLabel('left', 'パワースペクトル密度')

    def add_widgets_to_layout(self):
        """
        ウィジェットをレイアウトに配置
        """
        # ファイル選択用の水平レイアウト
        file_selection_layout = QHBoxLayout()
        file_selection_layout.addWidget(self.browse_button)
        file_selection_layout.addWidget(self.file_path_label)

        # グラフを左右に並べる水平レイアウト
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.time_series_plot)
        graph_layout.addWidget(self.psd_plot)

        # メインレイアウトに各レイアウトを追加
        self.main_layout.addLayout(file_selection_layout)
        self.main_layout.addLayout(graph_layout)