import requests
import urllib.parse
import json

from enum import Enum

class YouTubeFilters(Enum):
    TODAY = "EgIIAg%253D%253D"
    THIS_WEEK = "EgIIAw%253D%253D"
    THIS_MONTH = "EgIIBA%253D%253D"
    THIS_YEAR = "EgIIBQ%253D%253D"
    PLAYLIST = "EgIQAw%253D%253D"
    UNDER_4_MINUTES = "EgIYAQ%253D%253D"
    BETWEEN_4_AND_20_MINUTES = "EgIYAw%253D%253D"
    OVER_20_MINUTES = "EgIYAg%253D%253D"
    LIVE = "EgJAAQ%253D%253D"
    FOUR_K = "EgJwAQ%253D%253D"
    HD = "EgIgAQ%253D%253D"
    SUBTITLES_CC = "EgIoAQ%253D%253D"
    CREATIVE_COMMONS = "EgIwAQ%253D%253D"
    THREE_SIXTY = "EgJ4AQ%253D%253D"
    VR180 = "EgPQAQE%253D"
    THREE_D = "EgI4AQ%253D%253D"
    HDR = "EgPIAQE%253D"
    LOCATION = "EgO4AQE%253D"
    PURCHASED = "EgJIAQ%253D%253D"
    UPLOAD_DATE = "CAISAA%253D%253D"
    VIEW_COUNT = "CAMSAA%253D%253D"
    RATING = "CAESAA%253D%253D"

class YoutubeSearch:
    """
    Class to perform searches on YouTube and retrieve video information.

    Args:
        search_terms (str): The search terms to use for the YouTube search.
        max_results (int, optional): The maximum number of results to retrieve.

    Methods:
        _search: Perform the YouTube search based on the search terms and max results.
        _parse_html: Parse the HTML response from the YouTube search and extract video information.
        to_dict: Return the videos as a dictionary and optionally clear the cache.
        to_json: Return the videos as a JSON string and optionally clear the cache.
    """

    def __init__(self, search_terms: str, max_results=None, youtube_filter: str=None):
        """
        Initialize a YoutubeSearch object with search terms and optional maximum results.

        Args:
            search_terms (str): The search terms to use for the YouTube search.
            max_results (int, optional): The maximum number of results to retrieve.

        Returns:
            None
        """

        self.search_terms = search_terms
        self.max_results = max_results
        self.youtube_filter = youtube_filter
        self.videos = self._search()

    def _search(self):
        """
        Perform a search on YouTube based on the search terms and retrieve the search results.

        Args:
            None

        Returns:
            list: A list of dictionaries containing information about the search results.
        """
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        BASE_URL = "https://youtube.com"
        if self.youtube_filter:
            url = f"{BASE_URL}/results?search_query={encoded_search}&sp={self.youtube_filter}"
        else:
            url = f"{BASE_URL}/results?search_query={encoded_search}" 
        # print(url)
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self._parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def _parse_html(self, response):
        """
        Parse the HTML response from a YouTube search and extract video information.

        Args:
            response (str): The HTML response from the YouTube search.

        Returns:
            list: A list of dictionaries containing information about the videos extracted from the HTML response.
        """
        if data := self._extract_json_data(response):
            return (
                self._extract_playlist_info(data)
                if self.youtube_filter == YouTubeFilters.PLAYLIST.value
                else self._extract_video_info(data)
            )
        else:
            return []

    def _extract_json_data(self, response):
        """
        Extract JSON data from the HTML response.

        Args:
            response (str): The HTML response from the YouTube search.

        Returns:
            dict: JSON data extracted from the HTML response.
        """
        start = response.find("ytInitialData") + len("ytInitialData") + 3
        end = response.find("};", start) + 1
        json_str = response[start:end]
        return json.loads(json_str)

    def _extract_playlist_info(self, data):
        """
        Extract information about playlists from the JSON data.

        Args:
            data (dict): JSON data extracted from the HTML response.

        Returns:
            list: A list of dictionaries containing information about playlists.
        """
        results = []
        contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
        for content in contents:
            if "itemSectionRenderer" in content:
                playlists = content["itemSectionRenderer"]["contents"]
                for playlist in playlists:
                    if "playlistRenderer" in playlist:
                        playlist_data = playlist["playlistRenderer"]
                        res = {
                            "id": playlist_data.get('playlistId', None),
                            "thumbnails": [thumbnail.get("url", None) for thumbnail in playlist_data.get('thumbnails', [])],
                            "title": playlist_data.get('title', {}).get('simpleText', None),
                            "long_desc": None,
                            "channel": playlist_data.get('longBylineText', {}).get('runs', [{}])[0].get('text', None) if 'longBylineText' in playlist_data else None,
                            "duration": None,
                            "views": None,
                            "publish_time": None,
                            "url_suffix": '/playlist?list='+playlist_data.get('navigationEndpoint', {}).get('watchEndpoint', {}).get('playlistId', None)
                        }
                        results.append(res)
        return results

    def _extract_video_info(self, data):
        """
        Extract information about videos from the JSON data.

        Args:
            data (dict): JSON data extracted from the HTML response.

        Returns:
            list: A list of dictionaries containing information about videos.
        """
        results = []
        contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
        for content in contents:
            if "itemSectionRenderer" in content:
                videos = content["itemSectionRenderer"]["contents"]
                for video in videos:
                    if "videoRenderer" in video:
                        video_data = video["videoRenderer"]
                        res = {
                            "id": video_data.get("videoId", None),
                            "thumbnails": [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}])],
                            "title": video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None),
                            "long_desc": video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None),
                            "channel": video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None),
                            "duration": video_data.get("lengthText", {}).get("simpleText", 0),
                            "views": video_data.get("viewCountText", {}).get("simpleText", 0),
                            "publish_time": video_data.get("publishedTimeText", {}).get("simpleText", 0),
                            "url_suffix": video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                        }
                        results.append(res)
        return results


    def to_dict(self, clear_cache=True):
        """
        Convert the videos to a dictionary format and optionally clear the cache.

        Args:
            clear_cache (bool, optional): Flag to indicate whether to clear the cache after conversion.

        Returns:
            list: A list of dictionaries representing the videos.
        """

        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        """
        Convert the videos to a JSON string format and optionally clear the cache.

        Args:
            clear_cache (bool, optional): Flag to indicate whether to clear the cache after conversion.

        Returns:
            str: A JSON string representing the videos.
        """

        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result
