import pandas as pd 
import numpy as np 
import plotly.express as px 
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc

def generate_table(dataframe: pd.DataFrame, col_name: str, max_rows: int=5):
    df = dataframe.sort_values(col_name, ascending=False)
    usecols = ["timezone", "title", col_name, "thumbnailURL"]
    
    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in usecols])
        ), 
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in usecols
            ]) for i in range(max_rows)
        ])
    ], bordered=True, dark=True, hover=True, responsive=True, striped=True)
    
    
    
def sort_thumbnail_url(dataframe: pd.DataFrame, col_name: str):
    return dataframe.sort_values(col_name, ascending=False)["thumbnailURL"].values[0]
    
    
def create_table(dataframe: pd.DataFrame):
    return html.Div([
        html.H1(children="ランキング分析"),
        html.Hr(),
        html.P("全ての過去のデータからソートして出力します。"),
        # viewcount
        html.Div([
            html.H3(children="・最も再生された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "viewCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "viewCount"),
                width="100%", 
            )
        ]), 
        # likecount
        html.Div([
            html.H3(children="・最も高評価された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "likeCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "likeCount"),
                width="100%", 
            )
        ]), 
        # dislikecount
        html.Div([
            html.H3(children="・最も低評価された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "dislikeCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "dislikeCount"),
                width="100%", 
            )
        ]), 
    ], style={"margin-top": "70px"})


def create_rank_table(df, config, kwd):
    if config["DEBUG"]:
        usecols = ["channelTitle", "title", "viewCount", "thumbnailURL"]
        dfs = df[usecols]
        dfs = dfs.sort_values("viewCount", ascending=False)[:10]
    else:
        usecols = df.columns
        dfs = df.copy()
        dfs = dfs.sort_values("viewCount", ascending=False)
        
    table = dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in usecols])
        ), 
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in usecols
            ]) for i in range(dfs.shape[0])
        ])
    ], bordered=True, dark=True, hover=True, responsive=True, striped=True)
    
    return html.Div([
        html.H1(f"[{kwd}]での検索結果"),
        html.Hr(),
        table, 
        html.Img(
            src=dfs.iloc[0]["thumbnailURL"], 
            width="100%"
        ), 
        html.Img(
            src=dfs.iloc[1]["thumbnailURL"], 
            width="100%"
        ), 
        html.Img(
            src=dfs.iloc[2]["thumbnailURL"], 
            width="100%"
        ), 
    ], style={"margin-top": "70px"})