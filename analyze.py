from alchemyapi import AlchemyAPI
import json
import parse
from pprint import pprint

alchemyapi = AlchemyAPI()


def get_sentiment_score(text):
    if len(text) == 0:
        return -1000
    #print("getting sentiment for "+text)
    alchemyapi = AlchemyAPI()
    sentiment_object = alchemyapi.sentiment('text', text)
    #pprint(sentiment_object)
    if sentiment_object["docSentiment"]["type"] == "neutral":
        return 0
    return sentiment_object["docSentiment"]["score"]


def get_sentiments_by_month():
    html_file = open("data/messages.htm", 'r', encoding="utf8")
    text_by_time = parse.get_words_for_months(html_file)
    for year in text_by_time.keys():
        for month in text_by_time[year].keys():
            text_by_time[year][month] = get_sentiment_score(text_by_time[year][month])

    # create tsv file
    data = "date\tsentiment\n"
    for year in text_by_time.keys():
        for month in text_by_time[year].keys():
            sentiment = text_by_time[year][month]
            data += str(year)+"-"+month+"\t"+str(sentiment)+"\n"
    print(data)
    outfile = open("data.tsv","w")
    outfile.write(data)
    outfile.close()

    return text_by_time




get_sentiments_by_month()