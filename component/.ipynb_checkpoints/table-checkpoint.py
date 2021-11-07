import pandas as pd 
import numpy as np 
import plotly.express as px 
import dash_html_components as html
import dash_core_components as dcc 

def generate_table(dataframe: pd.DataFrame, col_name: str, max_rows: int=10):
    
    df = dataframe.sort_values(col_name, ascending=False)
    usecols = ["timezone", "title", "commentCount", "viewCount", "likeCount", "dislikeCount"]
    
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in usecols])
        ), 
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in usecols
            ]) for i in range(max_rows)
        ], style={"margin-top": "5px"})
    ])
    
    
def table(dataframe: pd.DataFrame, col_name: str, children: str):
    
    return html.Div([
        html.Div([
            html.H3(children=children, style={"font-weight": "bold"})
        ], style={"text-align": "center"}), 
        generate_table(dataframe, col_name)
    ], style={
        "padding": "20px", 
        "margin": "0px 20px",
        "box-shadow": "4px 4px 4px lightgrey",
        "border-radius": "5px",
    })