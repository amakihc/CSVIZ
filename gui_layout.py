# gui_layout.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtGui import QFont
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
        # アプリケーション名ラベルを作成
        self.app_title_label = QLabel("CSVIZ")
        title_font = QFont("Helvetica", 24, QFont.Bold)
        self.app_title_label.setFont(title_font)

        # ボタンとラベル
        self.browse_button = QPushButton("Select CSV File")
        self.browse_button.setFixedWidth(100)
        self.file_path_label = QLabel("No file selected")
        
        # チャンネル選択用のウィジェットを作成
        self.channel_label = QLabel("Select Channel:")
        self.channel_combo_box = QComboBox()
        self.channel_combo_box.setFixedWidth(200)

        # グラフウィジェット
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # フォントオブジェクトを作成
        font = QFont()
        font.setPointSize(20)

        self.time_series_plot = pg.PlotWidget()
        self.time_series_plot.setTitle("Time Series Plot")
        self.time_series_plot.setLabel('bottom', 'Time')
        self.time_series_plot.setLabel('left', 'Amplitude')
        self.time_series_plot.showGrid(x=True, y=True, alpha=0.3)
        self.time_series_plot.setBackground('w')
        
        self.time_series_plot.getPlotItem().getAxis('bottom').setPen('k')
        self.time_series_plot.getPlotItem().getAxis('left').setPen('k')
        
        self.time_series_plot.getPlotItem().getAxis('bottom').label.setFont(font)
        self.time_series_plot.getPlotItem().getAxis('left').label.setFont(font)
        self.time_series_plot.getPlotItem().getAxis('bottom').setTickFont(font)
        self.time_series_plot.getPlotItem().getAxis('left').setTickFont(font)


        self.psd_plot = pg.PlotWidget()
        self.psd_plot.setTitle("Power Spectral Density (PSD)")
        self.psd_plot.setLabel('bottom', 'Frequency (Hz)')
        self.psd_plot.setLabel('left', 'ASD')
        self.psd_plot.showGrid(x=True, y=True, alpha=0.3)
        self.psd_plot.setLogMode(x=True, y=True)
        self.psd_plot.setBackground('w')

        self.psd_plot.getPlotItem().getAxis('bottom').setPen('k')
        self.psd_plot.getPlotItem().getAxis('left').setPen('k')

        self.psd_plot.getPlotItem().getAxis('bottom').label.setFont(font)
        self.psd_plot.getPlotItem().getAxis('left').label.setFont(font)
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

        # チャンネル選択用の水平レイアウト
        channel_selection_layout = QHBoxLayout()
        channel_selection_layout.addWidget(self.channel_label)
        channel_selection_layout.addWidget(self.channel_combo_box)

        # 最上部の水平レイアウト（タイトル、ファイル選択、チャンネル選択）
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.app_title_label)
        top_layout.addStretch()
        top_layout.addLayout(file_selection_layout)
        top_layout.addStretch()
        top_layout.addLayout(channel_selection_layout)

        # グラフを左右に並べる水平レイアウト
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.time_series_plot)
        graph_layout.addWidget(self.psd_plot)

        # メインレイアウトに各レイアウトを追加
        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(graph_layout)