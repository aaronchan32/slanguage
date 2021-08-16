from pytrends.request import TrendReq
from datetime import date
import time
from multiprocessing import Pool

pytrends = TrendReq(hl='en-US', tz=360)
testData2 = ["Poggers", "booba", "deez nuts", "cringe", "monkas", "thicc", "cringe", "skinny legend", "brx", "bru", "leafy", "nightblue"]
category = "0"
location = ""
property = ""
currentDate = date.today().strftime("%Y-%m-%d")
past2Date = str( int(currentDate[:4]) - 2 ) + currentDate[4:]
timeframe = past2Date + " " + currentDate

def isTrend(kw):
    if isTrendFiveYear(kw):
        return(kw + ' is slang.')
    if isTrendTwoYear(kw):
        return(kw + ' is slang.')
    return kw + " isn't slang."

def isTrendTwoYear(keyword):
    pytrends.build_payload([keyword], category, timeframe, location, property)
    data = pytrends.interest_over_time()
    mean = round(data.mean(),2)
    avg = round(data[keyword][-52:].mean(),2)
    trend = round(((avg/mean[keyword])-1)*100,2)

    if trend > 15:
        return (True)
    return (False)

def isTrendFiveYear(keyword):
    timeframe = "today 5-y"

    pytrends.build_payload([keyword], category, timeframe, location, property)
    data = pytrends.interest_over_time()

    mean = round(data.mean(),2)
    avg = round(data[keyword][-130:].mean(),2)
    trend = round(((avg/mean[keyword])-1)*100,2)

    if trend > 15:
        return (True)
    return (False)    


if __name__ == "__main__":
    start_time = time.time()
    p = Pool()
    result = p.map(isTrend, testData2)
    print(result)

    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))