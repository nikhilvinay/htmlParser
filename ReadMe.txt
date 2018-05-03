#####################################         Read Me Please         ######################################

- To accomplish this task I have used scrapy module of Python.
- I'm assuming you have Ubuntu > 14.04 version installed on you machine
- Before running this program there are some system requirents packages needs to get installed . Use below comand if you don't have python , scrapy , and related dependencies


					####### Installation Guide #######
sudo apt-get install python ###Install Python
sudo apt-get install python-pip ###Required to install python packages

##Dependecies  required before installing scrapy
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev 

pip install scrapy ###Installing Scrapy to scrap & Extract Data from websites
					####### Installation Guide End Here #######


					####### Running Application Guide #######
					git clone https://github.com/nikhilvinay/htmlParser.git
					cd htmlParser/crickbuz/crickbuz/spiders
					scrapy crawl cricket

- After hitting this command there will be one file created at location
	 htmlParser/crickbuz/crickbuz/spiders/cricket.json
- This file will contain all data of perticular match in the link.
- If you want to trace or check the code go to below file at location
 	htmlParser/crickbuz/crickbuz/spiders/cricket.py

