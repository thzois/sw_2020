## Analysing Tesla Inc. stock price - The Social Web (Vrije Universiteit)
One of the most shorted stock this fiscal year on the market is [Tesla](https://www.tesla.com). At the end of January its short interest had reached 18% of its total available shares to trade. Controversial to 
this high volume of short positions, Tesla’s stock has been rising ever since its lowest stock price since 2014, on the 3rd of June 2019 with a close of $178.97. 
Before this time period Tesla had followed a sharp downward trend. Some of it could be explained by Elon Musk’s bad business attitude of announcing over optimistic 
false information on tweeter to take Tesla private. In addition financial reports (quarterly reports to be more exact) during different time 
periods and the loss of key personnel have more strongly influenced the movement of the stock price in 2019.

In the beginning of 2020 we see a financial chart of the company that follows an increasing parabolic trend ever since the 3rd of June 2019. With controversial topics like 
the release and presentation of Tesla’s cyber truck, during this period Tesla has had to face many bluders and experienced great success on the stock market. 
This research aims to look at the sentiment of Tesla followers on [Twitter](https://twitter.com) during important events/announcements made by the company or its CEO and find a relationship between 
Twitter sentiment and the state of the investors interest (expressed in the stock price) in the following 3 trading days. Afterwards, the research moves to investigate whether 
there are differences of sentiment within the demographics of the Twitter users for each analysed event/announcement: number of followers, geographic data, age, number of retweets 
on the topic (engagement) etc.

In this research we are interested in the following events:
- <strong>3rd of June 2019</strong>: Tesla reaches a new minimum of $178.97 since 2014. 
- <strong>24th of July 2019</strong>: Tesla suffers its worst day of the year after brutal earnings report and loss of technology chief.
- <strong>21st of November 2019</strong>: Tesla unveils its new cyber truck.
- <strong>4th of February 2020</strong>: Tesla reaches its highest stock price till date of $962.86.

### Requirements
- Install python3 and pip3
- Install requirements with 'pip3 install -r requirements.txt'

Note: in requirements.txt we are using the branch "premium-search" from [tweepy](https://github.com/tweepy/tweepy) repository. In a future release that branch 
will be merged into master. Hence, pip3 installation will fail and you will have to run "pip3 install tweepy". 
