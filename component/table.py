import pandas as pd 
import numpy as np 
import plotly.express as px 
import dash_html_components as html
import dash_core_components as dcc 

def generate_table(dataframe: pd.DataFrame, col_name: str, max_rows: int=5):
    
    df = dataframe.sort_values(col_name, ascending=False)
    usecols = ["timezone", "title", col_name, "thumbnailURL"]
    
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in usecols])
        ), 
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in usecols
            ]) for i in range(max_rows)
        ])
    ])
    
    
def sort_thumbnail_url(dataframe: pd.DataFrame, col_name: str):
    
    return dataframe.sort_values(col_name, ascending=False)["thumbnailURL"].values[0]
    
def create_table(dataframe: pd.DataFrame):
    
    return html.Div([
        html.H1(children="Ranking Top5", style={"background-color": "#003257", "color": "white"}), 
        # viewcount
        html.Div([
            html.P(children="最も再生された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "viewCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "viewCount"),
                width="850px", 
            )
        ]), 
        # likecount
        html.Div([
            html.P(children="最も高評価された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "likeCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "likeCount"),
                width="850px", 
            )
        ]), 
        # dislikecount
        html.Div([
            html.P(children="最も低評価された動画一覧を取得します。"), 
            html.Div([
                generate_table(dataframe, "dislikeCount")
            ]), 
            html.Img(
                src=sort_thumbnail_url(dataframe, "dislikeCount"),
                width="850px", 
            )
        ]), 
    ], style={"margin-top": "10px"})
