import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
import dash 
import dash_core_components as dcc 
import dash_html_components as html

def update_graph(df, col_name: str):
    x = df[["date", col_name]]
    x["date"] = pd.to_datetime(x["date"])
    x = x.groupby("date").sum()
    x["date"] = x.index 
    x.reset_index(drop=True, inplace=True)
    fig = px.line(x, x="date", y=col_name)
    fig.update_layout(transition_duration=500)
    return fig 


def support_transition(df, col_name: str):
    
    dfs = df[["date"]]
    dfs["year"] = df.date.apply(lambda x: int(x.split("-")[0]))

    fig = update_graph(df, col_name)
    return html.Div([
        html.P(children=col_name + " における推移"),
        html.Div([
            dcc.Graph(figure=fig, id="graph-transition-"+col_name), 
            dcc.Slider(id="year-slider-"+col_name, 
                      min=dfs["year"].min(), max=dfs["year"].max(), value=dfs["year"].max(), 
                      marks={str(year): str(year) for year in dfs["year"].unique()},
                      step=None),
        ])
    ])

def create_transition(df: pd.DataFrame, app: object):
    
    return html.Div([
        html.H1(children="グラフ", style={"background-color": "#003257", "color": "white"}),
        support_transition(df, "viewCount"),
        support_transition(df, "likeCount"), 
        support_transition(df, "dislikeCount"), 
    ])
    
