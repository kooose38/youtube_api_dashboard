import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd 
import numpy as np 

def create_holiday_component(df):
    dfs = []
    for col in ["viewCount", "likeCount", "dislikeCount"]:
        x = df.groupby("holiday").mean().loc[:, [col]]
        x["holiday"] = x.index 
        x.reset_index(drop=True, inplace=True)
        dfs.append(x)
    
    fig = go.Figure(data=[
        go.Bar(name="再生回数", x=dfs[0]["holiday"], y=dfs[0]["viewCount"]),
        go.Bar(name="ライク数", x=dfs[1]["holiday"], y=dfs[1]["likeCount"]),
        go.Bar(name="ディスライク数", x=dfs[2]["holiday"], y=dfs[2]["dislikeCount"]),
    ])
    fig.update_layout(template="plotly_dark", barmode="stack")
    
    return html.Div([
#         html.P(children=col_name+"における休日平均"),
        dcc.Graph(figure=fig)
    ])

def create_holiday(dataframe: pd.DataFrame):
    df = dataframe.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["holiday"] = df["date"].dt.dayofweek 
    df["holiday"] = df.holiday.apply(lambda x: "holiday" if x in [5, 6] else "working")
    
    return html.Div([
        html.H1(children="休日分析"),
        html.Hr(),
        html.P("平日、祝日における各数値データの集計を描画します。\n違いがあるかどうか確認できます。"),
        create_holiday_component(df)
    ], style={"margin-top": "70px"})