import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px 
import pandas as pd 
import numpy as np 

def create_holiday_component(df, col_name: str):
    x = df.groupby("holiday").mean().loc[:, [col_name]]
    x["holiday"] = x.index 
    x.reset_index(drop=True, inplace=True)
    
    fig = px.bar(x, x="holiday", y=col_name)
    
    return html.Div([
        html.P(children=col_name+"における休日平均"),
        dcc.Graph(figure=fig)
    ])

def create_holiday(dataframe: pd.DataFrame):
    df = dataframe.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["holiday"] = df["date"].dt.dayofweek 
    df["holiday"] = df.holiday.apply(lambda x: "holiday" if x in [5, 6] else "working")
    
    return html.Div([
        create_holiday_component(df, "viewCount"),
        create_holiday_component(df, "likeCount"),
        create_holiday_component(df, "dislikeCount"),
    ])