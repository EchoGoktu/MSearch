# youtube_search

Python function for searching for youtube videos to avoid using their heavily rate-limited API

To avoid using the API, this uses the form on the youtube homepage and scrapes the resulting page.

## Installation
```gh repo clone Malykz/youtube_search```
<br> or <br>
```pip install youtube-search```

## Quick Start
```py -m youtube-search "Train video" 12``` <br>
it'll return 12 data about "Train video" in JSON format in the terminal.


## Example Usage in Python script

For a basic search (and all of the current functionality), you can use the search tool as follows:

```pip install youtube-search```

```python
from youtube_search import YoutubeSearch

results = YoutubeSearch('search terms', max_results=10).to_json()

print(results)

# returns a json string

########################################

results = YoutubeSearch('search terms', max_results=10).to_dict()

print(results)
# returns a dictionary
```
