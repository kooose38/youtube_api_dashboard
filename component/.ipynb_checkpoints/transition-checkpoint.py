import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
import dash 
import dash_core_components as dcc 
import dash_html_components as html

def update_graph(df):
    dfs = []
    for col in ["viewCount", "likeCount", "dislikeCount"]:
        x = df[["date", col]]
        x["date"] = pd.to_datetime(x["date"])
        x = x.groupby("date").sum()
        x["date"] = x.index 
        x.reset_index(drop=True, inplace=True)
        dfs.append(x)
    fig = go.Figure(data=[
        go.Scatter(x=dfs[0]["date"], y=dfs[0]["viewCount"], name="再生回数", mode="lines"),
        go.Scatter(x=dfs[1]["date"], y=dfs[1]["likeCount"], name="ライク数", mode="lines"),
        go.Scatter(x=dfs[2]["date"], y=dfs[2]["dislikeCount"], name="ディスライク数", mode="lines"),
    ])
    fig.update_layout(template="plotly_dark")
    return fig 


def support_transition(df):
    dfs = df[["date"]]
    dfs["year"] = df.date.apply(lambda x: int(x.split("-")[0]))
    fig = update_graph(df)
    return html.Div([
            dcc.Graph(figure=fig, id="graph-transition"), 
            dcc.Slider(id="slider-transition", 
                      min=dfs["year"].min(), max=dfs["year"].max(), value=dfs["year"].max(), 
                      marks={str(year): str(year) for year in dfs["year"].unique()},
                      step=None),
    ])

def create_transition(df: pd.DataFrame, app: object):
    return html.Div([
        html.H1(children="推移分析"),
        html.Hr(),
        html.P("時系列データを描画します。\n時期によって変動があるかどうか確認することができます。"),
        support_transition(df),
    ], style={"margin-top": "70px"})
    
