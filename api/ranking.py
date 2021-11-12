import pandas as pd 
import numpy as np 
import datetime 
from apiclient.discovery import build
from apiclient.errors import HttpError
from typing import Dict 

class RankingYoutube(object):
    def __init__(self, config: Dict[str, str], kwd: str, interval_days: int=2, max_result: int=10):
        self.config = config 
        self.q = kwd 
        self.max_result = max_result 
        self.youtube = build(config["YOUTUBE_API_SERVICE_NAME"], 
                             config["YOUTUBE_API_VERSION"], 
                             developerKey=config["YOUTUBE_API_KEY"])
        self.interval_days = interval_days 

        self.main()

    def __doc__(self):
        """
        特定のキーワードを基に指定した期間での最も再生されている動画を取得するAPI
        結果はLINEに出力する

        """

        pass

    def main(self):
        today, now = self.get_datetime()
        data1 = self.get_most_view_count_video(now)
        print("1")
        data2 = self.get_statistic(data1, today)
        df = self.create_table(data1, data2)
        print("[INFO] successfully.")
        return df 
        
    def get_datetime(self):
        today = datetime.datetime.today()
        now = today - datetime.timedelta(days=self.interval_days)
        now = str(now).split()
        now = now[0] + "T" + now[1].split(".")[0] + "Z"
        return today, now 
        
    def get_most_view_count_video(self, now):
        search_response = self.youtube.search().list(
            q=self.q,
            part="snippet",
            order="viewCount", 
            regionCode="JP", 
            publishedAfter=now,
            maxResults=self.max_result
        ).execute()

        description = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                description.append((search_result["snippet"]["channelTitle"], search_result["snippet"]["title"], 
                                   search_result["snippet"]["thumbnails"]["medium"]))
        return description 

    def get_statistic(self, data, today):
        videoIds = [c for c, _, _, _ in data]
        statistics = []
        for id in videoIds:
            stats = self.youtube.videos().list(part="statistics", id=id).execute()["items"][0]["statistics"]
            if "viewCount" not in stats:
                stats["viewCount"] = 0 
            statistics.append(stats["viewCount"])
            del stats 
            
        return statistics


    def create_table(self, data1, data2):
        assert len(data1) == len(data2)
        
        columns = ["channelTitle", "title", "viewCount", "thumbnailURL"]
        
        df = pd.DataFrame({columns[0]: [c for c, _, _ in data1], 
                          columns[1]: [c for _, c, _ in data1], 
                          columns[2]: data2, 
                          columns[3]: [c for _, _, c in data1]})
        
        return df 
