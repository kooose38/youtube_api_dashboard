# Youtube分析サイト 

### 目的
チャンネルごとの統計値に従ってデータを取得し、分析結果をダッシュボードで表示します。  

### 使い方  
  
1.[youtube API](https://developers.google.cn/youtube/v3/getting-started?hl=ja)に従ってAPI_KEYを取得してください。  


2.youtubeチャンネルから`channel ID`を取得します。  
コマンドを実行します。パッケージをインストールしてください。  
一定時間後に`localhost`が立ち上がるのでアクセスします。

```
  $ python3 app.py 
  Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
    127.0.0.1 - - [08/Nov/2021 18:47:24] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_dash-dependencies HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_dash-layout HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_favicon.ico?v=2.0.0 HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_dash-component-suites/dash/dcc/async-plotlyjs.js HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_dash-component-suites/dash/dcc/async-slider.js HTTP/1.1" 200 -
    127.0.0.1 - - [08/Nov/2021 18:47:25] "GET /_dash-component-suites/dash/dcc/async-graph.js HTTP/1.1" 200 -
```  