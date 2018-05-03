# -*- coding: utf-8 -*-
import scrapy
import unicodedata


class CricketSpider(scrapy.Spider):
    name = 'cricket'
    allowed_domains = ['www.cricbuzz.com/live-cricket-scorecard/19873/indw-vs-engw-6th-match-womens-t20i-triseries-in-india-2018']
    start_urls = ['http://www.cricbuzz.com/live-cricket-scorecard/19873/indw-vs-engw-6th-match-womens-t20i-triseries-in-india-2018']

    ###########################################################################################################
    	#Below functin is main function from where execution get starts
    	#It will call other sub function who will be responsible for creation of final result
    ###########################################################################################################
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

    	allInningsInformation = self.getAllInningsInformation(response)
    	finalResponse["scoreCard"]["firstInning"] = allInningsInformation["firstInning"]
    	finalResponse["scoreCard"]["secondInning"] = allInningsInformation["secondInning"]
    	yield finalResponse
    	#return finalResponse
    ###########################################################################################################
    	#Below function is used for getting all Match information.It will get overall match summary
    	 
    ###########################################################################################################

    def parseMatchInformation(self, response):
    	titles = response.css('.cb-mtch-info-itm>div::text').extract()
    	match_result = response.css('.cb-scrcrd-status::text').extract()
        match_info = {}
        keys = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(titles) if i % 2 == 0]
        values = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(titles) if i % 2 != 0]
        match_info = dict(zip(keys, values))
        match_info["match_result"] = unicodedata.normalize('NFKD', match_result[0]).encode('ascii','ignore')
        return match_info;

    ###########################################################################################################
    	#Below function is used to get both innings information (First inning & Second inning)
    ###########################################################################################################

    def getAllInningsInformation(self , response):
    	firstInning = {"team":"","batsmen":[ ],"bowler":[ ] }
    	secondInning = {"team":"","batsmen":[ ],"bowler":[ ] }
    	
    	firstInningTeamInfo = response.css('#innings_1>div>div>span::text').extract()
    	firstInningTeamName = unicodedata.normalize('NFKD', firstInningTeamInfo[0]).encode('ascii','ignore')

    	secondInningTeamInfo = response.css('#innings_2>div>div>span::text').extract()
    	secondInningTeamName = unicodedata.normalize('NFKD', secondInningTeamInfo[0]).encode('ascii','ignore')
    	 
    	firstInning["team"] = firstInningTeamName
    	firstInningData  =  self.getBattingScoreCardInformation("innings_1" , response)
    	firstInning["bowler"] =  firstInningData["bowlerNames"]
    	firstInningbatsmen = self.createBatsmenData(firstInningData)
    	firstInning["batsmen"] = firstInningbatsmen

    	secondInning["team"] = secondInningTeamName
    	secondInningData  =  self.getBattingScoreCardInformation("innings_2" , response)
    	secondInning["bowler"] =  secondInningData["bowlerNames"]
    	secondInningBatsmen = self.createBatsmenData(secondInningData)
    	secondInning["batsmen"] =  secondInningBatsmen
    	
    	return {"firstInning" : firstInning , "secondInning" : secondInning}

    ###########################################################################################################
    	#Below function is used to create batsmen infromation
    	#Example how many runs he has score , how many bowls he has taken and so on.
    	#This function will take all batsmen data which will be get filtered as an output
    	#It will return list of dictionry
    ###########################################################################################################

    def createBatsmenData(self , inningsData):
    	batsmen = []
    	batsmentInformation ={"name" : "" , "dismisalType" : "" , "runs" : 0 , "ballsTaken" : 0 , "fours" : 0 , "six" : 0 , "strikeRate" : 0} 
    	batsmenNames = inningsData["batsmen"]
    	dismisalType = inningsData["dismisalType"]
    	runs = inningsData["runs"]
    	ballsTaken = inningsData["ballsTaken"]
    	fours = inningsData["fours"]
    	six = inningsData["six"]
    	strikeRate = inningsData["strikeRate"]
    	

    	for currentBatsmanIndex in range(len(batsmenNames)):
    		batsmentInformation["name"] =  batsmenNames[currentBatsmanIndex]
    		batsmentInformation["dismisalType"] = dismisalType[currentBatsmanIndex] if currentBatsmanIndex<len(dismisalType) else "Did Not Played"
    		batsmentInformation["runs"] = runs[currentBatsmanIndex] if currentBatsmanIndex<len(runs) else 0
    		batsmentInformation["ballsTaken"] =    ballsTaken[currentBatsmanIndex] if currentBatsmanIndex<len(ballsTaken) else 0
    		batsmentInformation["fours"] =   fours[currentBatsmanIndex] if currentBatsmanIndex<len(fours) else 0
    		batsmentInformation["six"] =  six[currentBatsmanIndex] if currentBatsmanIndex<len(six) else 0
    		batsmentInformation["strikeRate"] =  strikeRate[currentBatsmanIndex] if currentBatsmanIndex<len(strikeRate) else 0
    		batsmen.append(batsmentInformation.copy())
    		currentBatsmanIndex = currentBatsmanIndex+1
    	return batsmen
    ###########################################################################################################
    	#Below function is basically used for scrapping data from web page.
    	#It will take inning id as a parameter . 
    ###########################################################################################################

    def getBattingScoreCardInformation(self , inningsId , response):
    	batsmenNames = []
        bowlerNames = []
        dismisalType = []
        runs = []
        ballsTaken = []
    	dismisalType = response.css('#'+inningsId+'>div>.cb-scrd-itms>.cb-col>.text-gray::text').extract()
        fours = []
        six = []
        strikeRate = []
        parentDiv = response.css('#'+inningsId+'>.cb-ltst-wgt-hdr')

        for index, link in enumerate(parentDiv):
            if index ==0 :
                batsmenNames = link.css('.cb-scrd-itms>.cb-col>.cb-text-link::text').extract()
            else :
                bowlerNames = link.css('.cb-scrd-itms>.cb-col>.cb-text-link::text').extract()
        
        ##scrapping runs scored by each batsman
        for index, link in enumerate(parentDiv):
            if index == 0 :
                runs = link.css('.cb-scrd-itms>.cb-col.cb-col-8.text-right.text-bold::text').extract()
                runs = runs[:-2]

        ##scrapping ballsTaken by each batsman
        for index, link in enumerate(parentDiv):
            if index == 0 :
                ballsTaken = link.css('.cb-scrd-itms>:nth-child(4)::text').extract()

        ##scrapping fours
        for index, link in enumerate(parentDiv):
            if index == 0 :
                fours = link.css('.cb-scrd-itms>:nth-child(5)::text').extract()

        ##scrapping six
        for index, link in enumerate(parentDiv):
            if index == 0 :
                six = link.css('.cb-scrd-itms>:nth-child(6)::text').extract()

        for index, link in enumerate(parentDiv):
            if index == 0 :
                strikeRate = link.css('.cb-scrd-itms>:nth-child(7)::text').extract()

        batsmenNames = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(batsmenNames)]
        bowlerNames = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(bowlerNames)]
        dismisalType = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(dismisalType)]
        runs = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(runs)]
        ballsTaken = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(ballsTaken)]
        fours = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(fours)]
        six = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(six)]
        strikeRate = [unicodedata.normalize('NFKD', el).encode('ascii','ignore') for i, el in enumerate(strikeRate)]

        return {"batsmen" : batsmenNames , "bowlerNames" : bowlerNames , 
        "dismisalType" : dismisalType , "runs" : runs , "ballsTaken" : ballsTaken 
        , "fours" : fours , "six" : six , "strikeRate" : strikeRate}