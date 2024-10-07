from .youtube_search import YoutubeSearch


class TestSearch:

    def test_init_defaults(self):
        search = YoutubeSearch('test')
        assert search.max_results is None
        assert 1 <= len(search.videos)

    def test_init_max_results(self):
        search = YoutubeSearch('test', max_results=10)
        assert 10 == search.max_results
        assert 10 == len(search.videos)

    def test_dict(self):
        search = YoutubeSearch('test', max_results=10)
        assert isinstance(search.to_dict(), list)

    def test_json(self):
        search = YoutubeSearch('test', max_results=10)
        assert isinstance(search.to_json(), str)

    def test_clear_cache(self):
        search = YoutubeSearch('test', max_results=10)
        json_output = search.to_json(clear_cache=False)
        assert "" != search.videos

        dict_output = search.to_dict()
        assert "" == search.videos

    #-------------------------Async Tests---------------------#
    def test_init_max_results_async(self):
        queries = ['test' for _ in range(4)]
        search = YoutubeSearch(queries, max_results=10, num_workers=4)
        assert 10 == search.max_results
        for each_query_result in search.videos:
            assert 10 == len(each_query_result)

    def test_dict_async(self):
        queries = ['test' for _ in range(4)]
        search = YoutubeSearch(queries, max_results=10, num_workers=4)
        assert isinstance(search.to_dict(), list)

    def test_json_async(self):
        queries = ['test' for _ in range(4)]
        search = YoutubeSearch(queries, max_results=10, num_workers=4)
        assert isinstance(search.to_json(), str)

    def test_clear_cache_async(self):
        queries = ['test' for _ in range(4)]
        search = YoutubeSearch(queries, max_results=10, num_workers=4)
        json_output = search.to_json(clear_cache=False)
        assert "" != search.videos

        dict_output = search.to_dict()
        assert "" == search.videos