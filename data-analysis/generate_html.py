import json
import glob
import os


# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def remove_old_html_files():
    file_list = glob.glob('../web-app/event*.html') 
    for file_path in file_list:
        try:
            os.remove(file_path)
        except:
            print("Error while deleting file : ", file_path)


def generate_html(events):
    navbars = []
    statistics = []
    sentiment_vs_stock_charts = []
    sentiment_gauges = []
    files = []
    
    for i in range(1, len(events['events']) + 1):
        # navbar
        nav = ''
        # DO NOT MODIFY THE SPACING IN THE NAV STRING
        for j in range(1, len(events['events']) + 1):
            if i == j:
                # add style=color: white (active page)
                nav += f'\
         <li class="nav-item">\n \
            <a class="nav-link js-scroll-trigger" href="./event{j}.html" style="color: white">Event {j}</a>\n \
         </li>\n '
            else:
                nav += f'\
         <li class="nav-item">\n \
            <a class="nav-link js-scroll-trigger" href="./event{j}.html">Event {j}</a>\n \
         </li>\n '

        nav += f'\
         <li class="nav-item">\n \
            <a href="https://github.com/thzois/sw_2020" target="_blank"><img src="./images/github_white.png" width="110" alt="Fork me on GitHub"></a>\n \
         </li>\n '

        navbars.append(nav)
        files.append(open(f'../web-app/event{i}.html', 'w'))

        # statistics - open file for this event
        for event in events["events"]:
            filename = event["start_date"] + "_" + event["end_date"] + ".json"
            sentiment_vs_stock_charts.append("\t\t\t\t\t\tsentiment_vs_stock(ctx, '" + filename + "');\n")
            sentiment_gauges.append("\t\t\t\t\t\tsentiment_gauge(ctx, '" + filename + "');\n")

            with open("tweets/results/" + filename, "r") as twitter_file:
                twitterd = json.load(twitter_file)
                hashtags = ''
                for ht in event["hashtags"]:
                    # add 2 spaces
                    hashtags += ht + ' &nbsp;'

                # DO NOT MODIFY THE SPACING IN THE STATISTICS STRING
                statistics.append( 
    f'\
     <div class="row">\n \
        <div class="col-md-12 text-center">\n \
            <h3></br>{event["title"]}</h3>\n \
        </div>\n \
     </div>\n \
     <div class="row"><br></div>\n \
     <div class="row">\n \
         <div class="col-md-6">\n \
             <ul id="{event["start_date"]}_{event["end_date"]}" class="list-group-1">\n \
                 <li class="list-group-item active">Data collection information</li>\n \
                 <li class="list-group-item">Event start: <span class="highlight">{event["start_date"]}</span></li>\n \
                 <li class="list-group-item">Event end: &nbsp;<span class="highlight">{event["end_date"]}</span></li>\n \
                 <li class="list-group-item">Hashtags: <span class="highlight">{hashtags}</span></li>\n \
             </ul>\n \
         </div>\n \
         <div class="col-md-6">\n \
             <ul class="list-group">\n \
                 <li class="list-group-item active">Processing information</li>\n \
                 <li class="list-group-item">Total tweets: <span class="highlight">{twitterd["total_tweets"]}</span></li>\n \
                 <li class="list-group-item">Tweets with location: <span class="highlight">{twitterd["tweets_with_location"]}</span></li>\n \
                 <li class="list-group-item">Tweets with unknown location: <span class="highlight">{twitterd["tweets_disc_unknown_location"]}</span></li>\n \
                 <li class="list-group-item">Duplicate tweets: <span class="highlight">{twitterd["duplicate_tweets"]}</span></li>\n \
             </ul>\n \
         </div>\n \
     </div>\n \
     <div class="row"><br>\n \
         <div class="col-md-12 text-center"><br>\n \
             <h5>Tweets analyzed: <span class="highlight">{twitterd["tweets_stored"]}</span></h5>\n \
         </div>\n \
     </div>\n')


    with open('event_template.html') as event_template_file:
        for line in event_template_file:
            idx = 0
            for file in files:
                file.write(line)
                if '### SWAnalytics NAV' in line:
                    file.write(f'\t\t\t\t<ul class="navbar-nav ml-auto">\n {navbars[idx]} \t\t\t</ul>\n')
                if '### SWAnalytics STATISTICS' in line:
                    file.write(statistics[idx])
                if '### SWAnalytics SENTIMENT_STOCK' in line:
                    file.write(sentiment_vs_stock_charts[idx])
                if '### SWAnalytics SENTIMENT_GAUGE' in line:
                    file.write(sentiment_gauges[idx])
                idx += 1


def main():
    events = read_events()
    remove_old_html_files()
    generate_html(events)


if __name__ == "__main__":
    main()
