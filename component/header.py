import dash 
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd 
import numpy as np 

def create_header(df): 
    channelId = df["channelId"].values[0]
    channelTitle = df["channelTitle"].values[0]
    url = "https://www.youtube.com/channel/" + df["channelId"].values[0]
    videoCumsum =  df["videoId"].count().astype(str)
    viewCumsum = df["viewCount"].sum().astype(str)
    likeCumsum = df["likeCount"].sum().astype(str)
    dislikeCumsum = df["dislikeCount"].sum().astype(str)
    commentCumsum = df["commentCount"].sum().astype(str)
    viewAvg = df["viewCount"].mean().round(0).astype(str)
    likeAvg = df["likeCount"].mean().round(0).astype(str)
    dislikeAvg = df["dislikeCount"].mean().round(0).astype(str)
    commentAvg = df["commentCount"].mean().round(0).astype(str)
    
    return html.Div([
        html.H1(children="統計値"), 
        html.Hr(),
        html.P(children="チャンネル名: " + channelTitle), 
        html.P(children="URL: "),
        html.A(children=url, href=url), 
        html.P(children="総動画本数 : " + videoCumsum), 
        html.P(children="総視聴回数: " + viewCumsum), 
        html.P(children="総ライク数: " + likeCumsum), 
        html.P(children="総ディスライク数: " + dislikeCumsum), 
        html.P(children="総コメント数: " + commentCumsum), 
        html.P(children="平均視聴回数: " + viewAvg), 
        html.P(children="平均ライク数: " + likeAvg), 
        html.P(children="平均ディスライク数: " + dislikeAvg), 
        html.P(children="平均コメント数: " + commentAvg), 
    ])
    
    