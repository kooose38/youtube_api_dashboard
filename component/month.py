import dash 
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd 
import numpy as np 

def create_month_component(df, col_name):
    if col_name == "viewCount":
        fig = px.violin(df, y=col_name, x="month", template="plotly_dark")

        return html.Div([
            dcc.Graph(figure=fig),
        ])
    else:
        fig = go.Figure()
        fig.add_traces(go.Violin(x=df["month"], y=df["likeCount"], name="ライク数", line_color="blue",
                                legendgroup="likeCount", scalegroup="likeCount", side="positive"))
        fig.add_traces(go.Violin(x=df["month"], y=df["dislikeCount"], name="ディスライク数", line_color="orange",
                                legendgroup="dislikeCount", scalegroup="dislikeCount", side="negative"))
        fig.update_traces(meanline_visible=True)
        fig.update_layout(template="plotly_dark", violingap=0, violinmode="overlay")
        return html.Div([
            dcc.Graph(figure=fig)
        ])

def create_month(dataframe: pd.DataFrame):
    df = dataframe.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    
    most_popular_month = df.groupby("month").mean().loc[:, ["viewCount"]].sort_values("viewCount", ascending=False)
    most_popular_month["month"] = most_popular_month.index 
    most_popular_month.reset_index(drop=True, inplace=True)
    most_popular_month = most_popular_month.iloc[0]["month"]
    
    def calc_corr(df, target_col):
        return df[["viewCount", target_col]].corr().iloc[0, 1]
    
    like_corr = calc_corr(dataframe, "likeCount")
    dislike_corr = calc_corr(dataframe, "dislikeCount")
    if like_corr > dislike_corr:
        txt = "高評価と再生数に正の相関がみられ健康的です。"
    else:
        txt = "低評価と再生数に正の相関がみられ要注意です。"
        
    comment = dataframe["commentCount"].mean()
    if comment < 100.0:
        txt1 = "コメント数を増やしましょう。"
    else:
        txt1 = "十分なコメント数です。この調子で頑張ってください。"
        
    
    return html.Div([
        html.H1("月分析"),
        html.Hr(),
        html.P("月ベースに各数値を合計します。"),
        create_month_component(df, "viewCount"),
        create_month_component(df, "all"),
        
        html.Div([
            html.H1(children="診断結果"),
            html.Hr(),
            html.P(children="再生回数の多いのは、" + str(most_popular_month) + "月です"),
            html.P(children=txt),
            html.P(children=txt1)
        ], style={"margin-top": "70px"})
    ], style={"margin-top": "70px"})