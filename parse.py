from bs4 import BeautifulSoup, NavigableString
import pprint

html_file = open("data/messages.htm", 'r', encoding="utf8")
pp = pprint.PrettyPrinter(indent=4)


def initialize_months():
    return {"January":"","February":"","March":"","April":"","May":"","June":"","July":"","August":"","September":"","October":"","November":"","December":""}


def get_year_and_month(date):
    splitted = date.split(', ')
    month_and_day = splitted[1] # "April 3"
    month = month_and_day.split(' ')[0] # "April"
    year_and_time = splitted[2] # 2011 at 3:23pm CDT
    year = year_and_time.split(' ')[0]
    return int(year), month


def get_words_for_months(file):
    '''
    Gets all the words for a month.
    :param filename: input file (data/messages.htm)
    :return: 2D map: words[year][month] = "blah blah blah"
    '''
    # for each <message>, the body of the message is in the <p> right after it
    soup = BeautifulSoup(html_file, 'html.parser')
    matrix = {}
    for message in soup.find_all("div", { "class" : "message" }):
        # get the date contained in a <span class="meta">
        date = message.find("span", { "class" : "meta" }).text
        year, month = get_year_and_month(date)
        msg_body = message.findNext("p").text

        if year not in matrix.keys():
            matrix[year] = initialize_months()
            matrix[year][month] = msg_body
        else:
            matrix[year][month] += " " + msg_body
    #print(matrix.keys())
    #pp.pprint(matrix[2012]["June"])
    return matrix


#get_words_for_months(html_file)