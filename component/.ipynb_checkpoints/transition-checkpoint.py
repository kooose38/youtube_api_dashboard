import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import dash 
import dash_core_components as dcc 
import dash_html_components as html

def create_transition(df: pd.DataFrame, col_name: str):
    dfs = df.copy()
    dfs = dfs[["date", col_name]]
    dfs["trend"] = dfs[col_name].rolling(window=7).mean().fillna(dfs[col_name].mean())
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfs["date"], y=dfs[col_name], mode="lines", name=col_name))
    fig.add_trace(go.Scatter(x=dfs["date"], y=dfs["trend"], mode="lines", name="trend"))
    
    return html.Div([
        html.Div([
            html.H3(children=col_name + " transition", style={"fontsize": "12px"})
        ], style={"text-align": "center"}),
        html.Div([
            dcc.Graph(figure=fig)
        ])
    ], style={"justify-content": "space-between", "width": "33.3%"})

