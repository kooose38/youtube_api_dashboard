import dash 
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import argparse 
from dotenv import load_dotenv
import os 

from api import Youtube
from component.header import create_header
from component.table import create_table
from component.transition import create_transition
from component.word import create_word
from component.holiday import create_holiday
from component.month import create_month

load_dotenv()
app = dash.Dash(__name__)

parser = argparse.ArgumentParser(description='youtube analysis platform')
parser.add_argument("--channelId", help="youtube channel id", type=str)
parser.add_argument("--debug", help="developer only command", type=int, default=0)
args = parser.parse_args()

# データの取得
class YoutubeAPIConfig:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_API_VERSION = os.getenv("YOUTUBE_API_VERSION")
    YOUTUBE_API_SERVICE_NAME = os.getenv("YOUTUBE_API_SERVICE_NAME")
    DEBUG = True if args.debug == 0 else False

config = YoutubeAPIConfig()
if config.DEBUG:
    df = pd.read_csv("./csv/youtube_api.csv")
else:
    youtube = Youtube(config, args.channelId)
    df = youtube.main()
    df.to_csv(f"csv/{df['channelTitle'].values[0]}.csv", index=False)
    
# webページの作成関数
def container(df, app):
    return html.Div([
        create_table(df), 
        create_transition(df, app),
        create_word(df),
        create_holiday(df),
        create_month(df),
    ])

app.layout = html.Div([
    html.Div([
        html.H1(children="Youtube分析サイト", style={"font-size": "30px", "text-align": "center"}),
        create_header(df), 
        container(df, app)
    ], style={"width": "850px", "margin": "0px auto", "background-color": "white"})
], style={"background-color": "#003257", "margin": "0px"})

if __name__ == "__main__":
    app.run_server()