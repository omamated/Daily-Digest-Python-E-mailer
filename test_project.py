from project import scrape_news
import pytest

#make sure its a tuple/list and from HN
def test_scrape_news_hackernews():
    news = scrape_news("Hacker News")

    assert isinstance(news, list)
    assert len(news) <= 10

    if len(news) > 0:
        assert isinstance(news[0], tuple)
        assert len(news[0]) == 2

#make sure its a list from GOogle news
def test_scrape_news_google():
    news = scrape_news("Google News")

    assert isinstance(news, list)
    assert len(news) <= 10

    if len(news) > 0:
        assert isinstance(news[0][0], str)
        assert isinstance(news[0][1], str)

#make sure ap news and list
def test_scrape_news_ap():
    news = scrape_news("AP News")

    assert isinstance(news, list)
    assert len(news) <= 10
