import pandas as pd 
import numpy as np 
import datetime 
import requests 
import plotly.express as px 
from apiclient.discovery import build
from apiclient.errors import HttpError

class Youtube(object):
    def __doc__(self):
        """
        channel_idに基づいてyoutube_apiから過去全てのデータを取得する
        
        Args:
            config: Dict 設定
            channelId: str 
            
        Return:
            df: pd.DataFrame
        """
        
        pass
    
    def __init__(self, config, channelId):
        self.config = config 
        self.channelId = channelId
        self.youtube = build(config["YOUTUBE_API_SERVICE_NAME"], 
                             config["YOUTUBE_API_VERSION"], 
                             developerKey=config["YOUTUBE_API_KEY"])
        
    def main(self):
        data1 = self.get_video_ids()
        data2 = self.get_statistic(data1)
        df = self.create_dateframe(data1, data2)
        df = self.preprocess(df)
        return df 

    def preprocess(self, df):
        df["date"] = df.timezone.apply(lambda x: x.split("T")[0])
        df["commentCount"] = df.commentCount.astype(int)
        df["viewCount"] = df.viewCount.astype(int)
        df["likeCount"] = df.likeCount.astype(int)
        df["dislikeCount"] = df.dislikeCount.astype(int)
        return df 

    def get_video_ids(self):
        description = []
        nextPagetoken = "" 
        while True:
            if nextPagetoken != None:
                nextpagetoken = nextPagetoken
            search_response = self.youtube.search().list(
                channelId=self.channelId, 
                part="snippet",
                type="video",
                order="date", 
                maxResults=50,
                pageToken=nextpagetoken
                
            ).execute()
            
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    description.append((search_result["id"]["videoId"], search_result["snippet"]["channelId"],
                                        search_result["snippet"]["channelTitle"], search_result["snippet"]["title"], 
                                        search_result["snippet"]["publishTime"], search_result["snippet"]["thumbnails"]["medium"]["url"]))
            
            try:
                nextPagetoken = search_response["nextPageToken"]
            except:
                break 

        return description 

    def get_statistic(self, description):
        videoIds = [c for c, _, _, _, _, _ in description]
        statistics = []
        for id in videoIds:
            stats = self.youtube.videos().list(part="statistics", id=id).execute()["items"][0]["statistics"]
            if "commentCount" not in stats:
                stats["commentCount"] = 0 
            if "likeCount" not in stats:
                stats["likeCount"] = 0
            if "dislikeCount" not in stats:
                stats["dislikeCount"] = 0
            if "viewCount" not in stats:
                stats["viewCount"] = 0
            statistics.append((stats["commentCount"], stats["viewCount"], stats["likeCount"], stats["dislikeCount"]))
            del stats 
        return statistics 

    def create_dateframe(self, data1, data2):
        assert len(data1) == len(data2)

        columns = ["timezone", "videoId", "channelId", "channelTitle", "title", "thumbnailURL", 
                   "commentCount", "viewCount", "likeCount", "dislikeCount"]

        df = pd.DataFrame({columns[0]: [c for _, _, _, _, c, _ in data1], 
                           columns[1]: [c for c, _, _, _, _, _ in data1], 
                           columns[2]: [c for _, c, _, _, _, _ in data1], 
                           columns[3]: [c for _, _, c, _, _, _ in data1], 
                           columns[4]: [c for _, _, _, c, _, _ in data1], 
                           columns[5]: [c for _, _, _, _, _, c in data1], 
                           columns[6]: [c for c, _, _, _ in data2], 
                           columns[7]: [c for _, c, _, _ in data2], 
                           columns[8]: [c for c, _, c, _ in data2], 
                           columns[9]: [c for _, _, _, c in data2], 
                           })
        return df 