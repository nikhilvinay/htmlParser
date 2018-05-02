# -*- coding: utf-8 -*-
import scrapy
import unicodedata


class CricketSpider(scrapy.Spider):
    name = 'cricket'
    # allowed_domains = ['www.reddit.com/r/gameofthrones/']
    # start_urls = ['http://www.reddit.com/r/gameofthrones//']

    allowed_domains = ['www.cricbuzz.com/live-cricket-scorecard/19873/indw-vs-engw-6th-match-womens-t20i-triseries-in-india-2018']
    start_urls = ['http://www.cricbuzz.com/live-cricket-scorecard/19873/indw-vs-engw-6th-match-womens-t20i-triseries-in-india-2018']

    def parse(self, response):
    	finalResponse = {}
    	matchInformation = self.parseMatchInformation(response)
    	finalResponse["matchInformation"] = matchInformation
    	finalResponse["scoreCard"] =  {  
									      "firstInning":{  
									         "team":"",
									         "batsmen":[  

									         ],
									         "bowler":[  

									         ]
									      },
									      "secondInning":{  
									         "team":"",
									         "batsmen":[  

									         ],
									         "bowler":[  

									         ]
									      }
									   }

    	firstInningTeamName = self.getFirstInningsInformation(response)
    	#yield matchInformation;
    	#print "================================>"
        #Extracting the content using css selectors
        # titles = response.css('.title.may-blank::text').extract()
        # votes = response.css('.score.unvoted::text').extract()
        # times = response.css('time::attr(title)').extract()
        # comments = response.css('.comments::text').extract()
       
        # #Give the extracted content row wise
        # for item in zip(titles,votes,times,comments):
        #     #create a dictionary to store the scraped info
        #     scraped_info = {
        #         'title' : item[0],
        #         'vote' : item[1],
        #         'created_at' : item[2],
        #         'comments' : item[3],
        #     }

        #     #yield or give the scraped info to scrapy
        #     yield scraped_info

        
        #Give the extracted commentsntent row wise
        # for item in zip(titles):
        #     #create a dictionary to store the scraped info
        #     #print "--->" , item[0]
        #     scraped_info = {
        #         'title' : item[0],
        #     }

        #     #yield or give the scraped info to scrapy
        #     yield scraped_info
    def parseMatchInformation(self, response):
    	titles = response.css('.cb-mtch-info-itm>div::text').extract()
    	match_result = response.css('.cb-scrcrd-status::text').extract()
        match_info = {}
        keys = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(titles) if i % 2 == 0]
        values = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(titles) if i % 2 != 0]
        match_info = dict(zip(keys, values))
        match_info["match_result"] = unicodedata.normalize('NFKD', match_result[0]).encode('ascii','ignore')
        return match_info;

    def getFirstInningsInformation(self , response):
    	firstInning = {"team":"","batsmen":[ ],"bowler":[ ] }
		#batsmaninformation = { "name" : "" ,"dismissType" : "" , "run" : 0 , "balls" : 0 , "fours" : 0 , "six" : 0 , "strikeRate" : 0}

    	firstInningTeamInfo = response.css('#innings_1>div>div>span::text').extract()
    	firstInningTeamName = unicodedata.normalize('NFKD', firstInningTeamInfo[0]).encode('ascii','ignore')
    	 
    	inningsId = "innings_1"
    	self.getBattingScoreCardInformation(inningsId , response)

    	return firstInningTeamName
    def getBattingScoreCardInformation(self , inningsId , response):
    	# NameOfBatsman = response.css('#'+inningsId+'>div>.cb-scrd-itms>.cb-col>.cb-text-link::text').extract()
    	# dismisalType = response.css('#'+inningsId+'>div>.cb-scrd-itms>.cb-col>.text-gray::text').extract()
    	# runs = response.css('#'+inningsId+'>div>.cb-scrd-itms>.cb-col.cb-col-8.text-right.text-bold::text').extract()
    	# ballsTaken = response.css('#'+inningsId+'>div>.cb-scrd-itms>:nth-child(4)::text').extract()
    	NameOfBatsman = response.css('#'+inningsId+'>div>.cb-scrd-itms:nth-child(2)').extract()
    	print "Name Of batsman================>" , NameOfBatsman
