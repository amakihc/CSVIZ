# gui_layout.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
import pyqtgraph as pg
from PyQt5.QtGui import QFont

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
        # 全てのグラフに適用される設定
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # フォントオブジェクトを作成
        font = QFont()
        font.setPointSize(20) # 10ptに設定

        self.time_series_plot = pg.PlotWidget()
        self.time_series_plot.setTitle("時系列プロット")
        self.time_series_plot.setLabel('bottom', '時間')
        self.time_series_plot.setLabel('left', '振幅')
        # グリッドを灰色で有効化
        self.time_series_plot.showGrid(x=True, y=True, alpha=0.3)
        # グラフの色を白黒に設定
        self.time_series_plot.setBackground('w')
        
        # 目盛りと軸ラベルのスタイル設定
        self.time_series_plot.getPlotItem().getAxis('bottom').setPen('k')
        self.time_series_plot.getPlotItem().getAxis('left').setPen('k')
        
        # 軸ラベルのフォントサイズを設定
        self.time_series_plot.getPlotItem().getAxis('bottom').label.setFont(font)
        self.time_series_plot.getPlotItem().getAxis('left').label.setFont(font)

        # 目盛り数字のフォントサイズを設定
        self.time_series_plot.getPlotItem().getAxis('bottom').setTickFont(font)
        self.time_series_plot.getPlotItem().getAxis('left').setTickFont(font)


        self.psd_plot = pg.PlotWidget()
        self.psd_plot.setTitle("パワースペクトル密度 (PSD)")
        self.psd_plot.setLabel('bottom', '周波数 (Hz)')
        self.psd_plot.setLabel('left', 'ASD')
        # グリッドを灰色で有効化
        self.psd_plot.showGrid(x=True, y=True, alpha=0.3)
        # 対数スケールに変更
        self.psd_plot.setLogMode(x=True, y=True)
        # グラフの色を白黒に設定
        self.psd_plot.setBackground('w')

        # 目盛りと軸ラベルのスタイル設定
        self.psd_plot.getPlotItem().getAxis('bottom').setPen('k')
        self.psd_plot.getPlotItem().getAxis('left').setPen('k')

        # 軸ラベルのフォントサイズを設定
        self.psd_plot.getPlotItem().getAxis('bottom').label.setFont(font)
        self.psd_plot.getPlotItem().getAxis('left').label.setFont(font)

        # 目盛り数字のフォントサイズを設定
        self.psd_plot.getPlotItem().getAxis('bottom').setTickFont(font)
        self.psd_plot.getPlotItem().getAxis('left').setTickFont(font)

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