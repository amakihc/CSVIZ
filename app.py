# app.py

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui_layout import UILayout
from data_processor import load_csv_data, compute_psd
import sys
import numpy as np

class App(QMainWindow):
    """
    アプリケーションのメインウィンドウクラス
    """
    def __init__(self):
        super().__init__()
        self.ui = UILayout()
        self.setCentralWidget(self.ui)
        self.setGeometry(100, 100, 1200, 600)

        self.df = None
        self.sampling_rate = 0
        
        # UIコンポーネントをAppクラスに追加
        self.ui.browse_button.clicked.connect(self.browse_file)
        # gui_layoutで作成されたチャンネル選択のコンボボックスに接続
        self.ui.channel_combo_box.currentIndexChanged.connect(self.plot_selected_channel)

    def browse_file(self):
        """
        ファイルダイアログを開き、CSVファイルを選択する
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.ui.file_path_label.setText(file_path)
            self.process_file(file_path)

    def process_file(self, file_path):
        """
        ファイルを処理し、ドロップダウンリストを更新する
        """
        self.df, self.sampling_rate = load_csv_data(file_path)
        if self.df is None or self.df.empty:
            return

        # ドロップダウンリストを更新
        self.ui.channel_combo_box.clear()
        
        # 最初の列は時間データなので、2列目からドロップダウンリストに追加
        num_columns = len(self.df.columns)
        channel_names = [f"Column {i+1}" for i in range(1, num_columns)]
        self.ui.channel_combo_box.addItems(channel_names)

        # 最初のチャンネルのデータを自動でプロット
        self.plot_selected_channel()
    
    def plot_selected_channel(self):
        """
        ドロップダウンリストで選択されたチャンネルのデータをプロットする
        """
        selected_index = self.ui.channel_combo_box.currentIndex()
        
        # インデックスが有効か確認 (ドロップダウンリストが空でないか)
        if selected_index < 0 or self.df is None:
            return

        # 選択された列のインデックス（0ベース）を取得
        # 最初の列は時間データなので、選択されたインデックスに1を足す
        data_column_index = selected_index + 1
        
        signal_data = self.df.iloc[:, data_column_index].values
        time_data = self.df.iloc[:, 0].values

        # データをプロット
        self.plot_time_series(time_data, signal_data)
        self.plot_psd(signal_data)
        
    def plot_time_series(self, time_data, signal_data):
        """
        時系列データをグラフにプロットする
        """
        self.ui.time_series_plot.clear()  # 既存のプロットをクリア
        # プロットの色を青に設定
        self.ui.time_series_plot.plot(time_data, signal_data, pen='b')
        
    def plot_psd(self, data):
        """
        PSDを計算し、グラフにプロットする
        """
        frequencies, psd = compute_psd(data, self.sampling_rate)
        
        self.ui.psd_plot.clear()  # 既存のプロットをクリア
        if len(frequencies) > 0 and len(psd) > 0:
            # プロットの色を青に設定
            self.ui.psd_plot.plot(frequencies, psd, pen='b')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())