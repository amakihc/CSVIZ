import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from scipy.signal import welch

# ----------------- 設定項目 -----------------
# 可視化したいCSVファイルへのパス
file_path = 'MokuPIDControllerData_20250620_144939.csv'
# CSVのヘッダーがある行のインデックス (0から始まる)
header_row = 10
# ---------------------------------------------

# Dashアプリケーションの初期化
app = dash.Dash(__name__)
server = app.server

# エラー発生時のグラフのプレースホルダーを定義
initial_fig = go.Figure(
    layout=go.Layout(
        template='plotly_dark',
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[
            {
                'text': 'エラーが発生しました',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }
        ]
    )
)

try:
    # CSVファイルの読み込み
    df = pd.read_csv(file_path, header=header_row)

    # サンプリング周波数の計算
    sample_period = df.iloc[1, 0] - df.iloc[0, 0]
    if sample_period == 0:
        raise ValueError("時間列のデータが重複しています。")
    fs = 1.0 / sample_period

    # 時系列データのグラフ
    time_series_fig = go.Figure(
        data=[go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1], mode='lines')],
        layout=go.Layout(
            template='plotly_dark',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Amplitude'},
        )
    )

    # パワースペクトル密度（PSD）の計算
    data = df.iloc[:, 1]
    f, Pxx = welch(data, fs, nperseg=1024)

    # PSDのグラフ
    psd_fig = go.Figure(
        data=[go.Scatter(x=f, y=Pxx, mode='lines')],
        layout=go.Layout(
            template='plotly_dark',
            xaxis={'title': 'Frequency', 'type': 'log'},
            yaxis={'title': 'PSD', 'type': 'log'},
        )
    )
    
    # 正常終了時のレイアウト
    app.layout = html.Div(
        style={
            'padding': '20px',
            'backgroundColor': '#222',
            'color': 'white',
            'font-family': 'sans-serif'
        },
        children=[
            html.H1("CSVIZ", style={'textAlign': 'center'}),
            html.Div(
                style={'display': 'flex'},
                children=[
                    html.Div(
                        dcc.Graph(
                            figure=time_series_fig, 
                            style={'height': '80vh'}
                        ), 
                        style={'width': '50%'}
                    ),
                    html.Div(
                        dcc.Graph(
                            figure=psd_fig, 
                            style={'height': '80vh'}
                        ), 
                        style={'width': '50%'}
                    ),
                ]
            )
        ]
    )

except Exception as e:
    # エラー発生時のレイアウト
    app.layout = html.Div(
        style={
            'padding': '20px',
            'backgroundColor': '#222',
            'color': 'white',
            'font-family': 'sans-serif'
        },
        children=[
            html.H1("エラー", style={'textAlign': 'center'}),
            html.P(f"ファイルの処理中にエラーが発生しました: {e}"),
            html.P("CSVファイルの形式が正しいか、ヘッダーの設定が正しいか確認してください。")
        ]
    )

if __name__ == '__main__':
    app.run(debug=True)