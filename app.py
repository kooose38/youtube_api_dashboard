import dash 
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import argparse 
import os 
import datetime 

from api import Youtube
from component.nav import create_navbar 
from component.header import create_header
from component.table import create_table
from component.transition import create_transition
from component.word import create_word
from component.holiday import create_holiday
from component.month import create_month

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# データの取得
config = {
    "YOUTUBE_API_VERSION": "v3",
    "YOUTUBE_API_SERVICE_NAME": "youtube",
    "DEBUG": False,
    "data": pd.read_csv("./csv/youtube_api.csv"), 
}

    
# 初期画面
api_input = dbc.FormGroup([dbc.Label("API Key", html_for="example-api-key", width=2)
                    , dbc.Col(dbc.Input(type="text"
                                        , id="example-api-key"
                                        , placeholder="Enter API KEY") #end input
                                , width=10) #end col
                        ], row=True)#end formgroup
channel_input = dbc.FormGroup([dbc.Label("Channel ID", html_for="example-channel-id", width=2)
                    ,dbc.Col(dbc.Input(type="text"
                                        , id="example-channel-id"
                                        , placeholder="Enter Channel ID"
                                        , maxLength = 80)#end input
                            , width=10) #end column
                    ],row=True)#end form group

index_page = html.Div([
    create_navbar(),
    dbc.Container([
        html.Div([
            html.P("Youtube API Keyを取得してください。"),
            html.P("APIから入手できるデータには利用上限があるので検索時に注意してください。"),
            html.A("・キーを取得する", href="https://developers.google.cn/youtube/v3/getting-started?hl=ja"),
            html.Br(),
            html.A("・ソースコードはこちらから", href="https://github.com/kooose38/youtube_api_dashboard"),
        ], style={"margin": "20px 0px"}), 
        html.Br(),
        dbc.Card(dbc.CardBody([dbc.Form([api_input, channel_input])])), 
        html.Div(id="div-btn", children=[
            dbc.Alert("入力してください", color="primary")
        ])
    ])
], style={"margin": "0px", "height": "500px"})
# 検索ボタンのイベント
@app.callback([Output("div-btn", "children")],
              [Input("example-api-key", "value"),
              Input("example-channel-id", "value")]
)
def update_input_data(api_key, channel_id):
    if (api_key != None) and (channel_id != None):
        config["YOUTUBE_API_KEY"] = api_key 
        config["SEARCH_CHANNEL_ID"] = channel_id
        
        try:
            if config["DEBUG"]:
                df = pd.read_csv("./csv/youtube_api.csv")
            else:
                youtube = Youtube(config, channel_id)
                df = youtube.main()
                
                # 履歴を保存する
                now = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
                db = pd.read_csv("./csv/db.csv")
                db = db.append({"timestamp": now, "channel": channel_id}, ignore_index=True)
                db.to_csv("./csv/db.csv", index=False)
                del db 
                
            config["data"] = df
            return [dbc.Alert([
                        dcc.Link(f"{df['channelTitle'].values[0]}で検索する", href=f"/search?q={channel_id}&api={api_key}")
                    ], color="primary")]
        except Exception as e:
            print(f"[ERROR]: {print(e)}")
            return [dbc.Alert("存在しません", color="danger")]
    else:
        return [dbc.Alert("入力してください", color="primary")]

    
# 検索後ページ
def container(df, app):
    return html.Div([
        create_table(df), 
        create_transition(df, app),
        create_word(df),
        create_holiday(df),
        create_month(df),
        dcc.Link("検索ページに戻る", href="/")
    ])

def build_main_page():
    search_page = html.Div([
        create_navbar(),
        dbc.Container([
            create_header(config["data"]), 
            container(config["data"], app)
        ])
    ], style={"margin": "0px"})
    return search_page



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
@app.callback(Output("page-content", "children"), 
             [Input("url", "pathname")])
def display_page(pathname):
    if pathname.find("/search") >= 0:
        return build_main_page() 
    else:
        return index_page 


if __name__ == "__main__":
    app.run_server(debug=True)