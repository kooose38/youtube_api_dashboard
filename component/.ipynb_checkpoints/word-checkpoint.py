import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
from wordcloud import WordCloud
import base64
from io import BytesIO
from janome.tokenizer import Tokenizer

j_t = Tokenizer()
except_word = ["[", "]", "#", "?", "_", "!", "%", "&"]

def create_word_cloud(titles):
    word2count = {}
    for title in titles:
        for text in j_t.tokenize(title, wakati=True):
            if text in except_word:
                continue 
            if text not in word2count:
                word2count[text] = 1 
            else:
                word2count[text] += 1 
    
    return word2count 

def make_img(df):
    img = BytesIO()
    d = create_word_cloud(df["title"])
    wc = WordCloud(background_color="white", width=850, height=450).fit_words(d)
    wc.to_image().save(img, format="PNG")
    return "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())

def create_word(df):
    return html.Div([
        html.H1(children="テキスト分析"),
        html.Hr(),
        html.P("タイトルに頻出される単語を大小順に描画します。"),
        html.Img(src=make_img(df), width="100%")
    ], style={"margin-top": "70px"})
