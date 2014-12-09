listenScraper
===============

A scrapy crawler for lastFM listening history for a given user

TODO:
- Add a pipeline (can just use -o for now)

USAGE:
scrapy crawl lastfm -a apikey=YOURAPIKEY -a user=lastfmuser -o listens.json -L INFO
