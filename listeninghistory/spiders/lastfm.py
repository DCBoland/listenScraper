from scrapy.spider import Spider
from scrapy.selector import Selector
from listeninghistory.items import TrackListen
from scrapy.http import Request, Response, FormRequest
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class LastFMCrawler(Spider):
    name = "lastfm"
    allowed_domains = ["last.fm","audioscrobbler.com"]
    start_urls = ["https://secure.last.fm/login"]
    
    def __init__(self, apikey=None, user=None, loginUser=None, loginPassword=None, *args, **kwargs):
        super(LastFMCrawler, self).__init__(*args, **kwargs)
        self.apikey = apikey
        self.user = user
        self.loginUser = loginUser
        self.loginPassword = loginPassword
    
    def parse(self, response):        
        sel = Selector(response)
        
        return [FormRequest.from_response(response,
                    formxpath='//form[@action="/login"]',
                    formdata={'username': self.loginUser, 'password': self.loginPassword},
                    callback=self.after_login)]
        
    def after_login(self, response):
        from scrapy.shell import inspect_response
        #inspect_response(response)
        URL = "http://www.last.fm/user/" + self.user + "/tracks?view=compact&page=1"
        yield Request(URL, self.parseListeningHistory)

    def parseListeningHistory(self, response):
        sel = Selector(response)
        
        self.parseScrobbles(response)
        
        pageCount = int(sel.css('.btn.btn--small.btn--white:not(.iconright)::text')[-1].extract())
            
        for i in range(2,pageCount):
            URL = "http://www.last.fm/user/" + self.user + "/tracks?view=compact&page=" + str(i)
            yield Request(URL, self.parseScrobbles)    
        
    def parseScrobbles(self, response):
        sel = Selector(response)
        scrobbles = sel.css('.js-scrobble')
        for s in scrobbles:
            try:
                t = TrackListen()
                t['track'] = s.css('.spotify-inline-play-button::attr(data-uri)')[0].extract().replace('spotify:track:', '')
                t['date'] = s.css('.dateCell time::attr(datetime)')[0].extract()
                yield t
            except:
                # Probably no spotify URI
                pass