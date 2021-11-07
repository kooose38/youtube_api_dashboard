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
from component.word import create_word_detail, create_word_graph
from component.table import table
from component.transition import create_transition
from component.tag import create_tag 

load_dotenv()
app = dash.Dash(__name__)

parser = argparse.ArgumentParser(description='youtube analysis platform')
parser.add_argument("--channelId", help="youtube channel id", type=str)
args = parser.parse_args()

class YoutubeAPIConfig:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_API_VERSION = os.getenv("YOUTUBE_API_VERSION")
    YOUTUBE_API_SERVICE_NAME = os.getenv("YOUTUBE_API_SERVICE_NAME")
    DEBUG = True

config = YoutubeAPIConfig()
if config.DEBUG:
    df = pd.read_csv("./csv/youtube_api.csv")
else:
    youtube = Youtube(config, args.channelId)
    df = youtube.main()
    df.to_csv(f"csv/{df['channelTitle'].values[0]}.csv", index=False)


def header(title):
    return html.Div([
        html.H1(children="Channel Title: " + title, style={"font-weight": "bold"})
    ], style={"margin": "10px 40px"})

def container(df, app):
    return html.Div([
        html.Div([
            html.Div([
                create_tag("視聴回数", df.viewCount.mean().round(0), app), 
                create_tag("ライク数", df.likeCount.mean().round(0), app), 
                create_tag("ディスライク数", df.dislikeCount.mean().round(0), app), 
                create_tag("コメント数", df.commentCount.mean().round(0), app), 
            ], style={'display': 'flex', 'margin': '0px 0px 30px 0px'}), 
             html.Div([
                 create_transition(df, "viewCount"),
                 create_transition(df, "likeCount"),
                 create_transition(df, "dislikeCount"),
             ], style={
                 "display": "flex",
                 "padding": "20px",
                 "margin": "50px 20px",
                 "box-shadow": "4px 4px 4px lightgrey", 
                 "border-radius": "5px",
             }), 
            html.Div([
                create_word_detail(), 
                create_word_graph(df)
            ], style={
                "padding": "20px", 
                "margin": "50px 20px", 
                "box-shadow": "4px 4px 4px lightgrey", 
                "border-radius": "5px",
            })
        ], style={"width": "50%", "justify-content": "space-between", "height": "900px"}), 

        html.Div([
           table(df, "viewCount", "最も再生された動画一覧"),
           table(df, "likeCount", "最も高評価の動画一覧"),
           table(df, "dislikeCount", "最も低評価の動画一覧"),
        ], style={"width": "50%", "justify-content": "space-between", "height": "900px"})

    ], style={
        "display": "flex",
        "width": "100%", 
        "margin": "10px 40px",
    })

app.layout = html.Div([
    header(df["channelTitle"].values[0]), 
    container(df, app)
])

if __name__ == "__main__":
    app.run_server()