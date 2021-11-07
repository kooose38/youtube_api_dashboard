import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go

def create_word_cloud(titles):
    word2count = {}
    for title in titles:
        for text in title.split():
            if text not in word2count:
                word2count[text] = 1 
            else:
                word2count[text] += 1 
    
    word_df = pd.DataFrame({"word": [c for c, _ in word2count.items()], 
                            "count": [c for _, c in word2count.items()]})
    word_df = word_df.sort_values("count", ascending=False)[:10]
    return word_df 

def create_word_detail():
    return html.Div([
         html.H3(children="テキスト分析"),
        html.P(children="視聴回数に基づいて頻出される単語をタイトルからカウントします。"),
        html.P(children="平均視聴回数以上か、以下によって分離されています。")
    ], style={"text-align": "center"})

def create_word_graph(df: pd.DataFrame):
    mu = df["viewCount"].mean()
    up = df.loc[df["viewCount"] >= mu, ["cln_title"]]
    down = df.loc[df["viewCount"] < mu, ["cln_title"]]
    
    up = create_word_cloud(up["cln_title"])
    down = create_word_cloud(down["cln_title"])
    
    fig_up = px.bar(up, x="word", y="count")
    fig_down = px.bar(down, x="word", y="count")
    
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig_up)
        ], style={"justify-content": "space-between", "width": "50%"}), 
        html.Div([
            dcc.Graph(figure=fig_down)
        ], style={"justify-content": "space-between", "width": "50%"}), 
    ], style={"display": "flex"})
    