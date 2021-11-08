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
        html.H1(children="統計値", style={"color": "white", "background-color": "#003257"}), 
        html.P(children="ChannelId: " + channelId), 
        html.P(children="ChennelTitle: " + channelTitle), 
        html.P(children="URL: "),
        html.A(children=url, href=url), 
        html.P(children="Cumulative number of Videos : " + videoCumsum), 
        html.P(children="Total number of Views: " + viewCumsum), 
        html.P(children="Total number of Like counts: " + likeCumsum), 
        html.P(children="Total number of Dislike counts: " + dislikeCumsum), 
        html.P(children="Total number of Comment counts: " + commentCumsum), 
        html.P(children="Average number of Views: " + viewAvg), 
        html.P(children="Average number of Like counts: " + likeAvg), 
        html.P(children="Average number of Dislike counts: " + dislikeAvg), 
        html.P(children="Average number of Comment counts: " + commentAvg), 
    ])
    
    