from pytrendsasync.request import TrendReq
from datetime import date
import time
import asyncio
from multiprocessing import Pool


slangTrend = TrendReq(timeout=(10, 25), retries=2, backoff_factor=0.1)
category = "0"
location = ""
property = ""
timeframe = "today 5-y"
# testData2 = ["Poggers", "booba", "deez nuts", "monkas", "thicc", "cringe", "skinny legend", "brx", "bru", "leafy", "nightblue", "normie", "hello", "water"]


async def get_Slang(wordList):
    # try :
    start_time = time.time()
    responses = await asyncio.gather(*[relatedSlang(kw) for kw in wordList])
    print("get_Slang --- %s seconds ---" % (time.time() - start_time))
    return list(filter(None, responses))
    # except:
    #     print("uh oh stinky")
    #     return []


async def relatedSlang(keyword):
    await slangTrend.build_payload([keyword], category, timeframe, location, gprop=property)
    data = await slangTrend.related_queries()
    if data[keyword]["top"] is not None:
        relatedQueriesString = ' '.join(
            data[keyword]["top"]["query"].iloc[0:11])
        if "mean" in relatedQueriesString or "definition" in relatedQueriesString:
            return keyword
        return None 
    return None


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# print(asyncio.run(get_Slang(testData2)))

# print("--- %s seconds ---" % (time.time() - start_time))
