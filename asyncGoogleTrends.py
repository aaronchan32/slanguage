from pytrends.request import TrendReq
from datetime import date
import time, sys, asyncio

#timeout=(10, 25)
slangTrend = TrendReq(requests_args= {'headers': {'Cookie': "SEARCH_SAMESITE=CgQI7JYB; HSID=AEZTVDFg8kha4Aa6F; SSID=A2Oj_JSoqvxhYLSGa; APISID=9M_JwAf_IlidvXhw/AoUFdX7ud8L2dL6n6; SAPISID=tytCQr3bNWOVqwFK/AprY7acK6lWfuLBya; __Secure-1PAPISID=tytCQr3bNWOVqwFK/AprY7acK6lWfuLBya; __Secure-3PAPISID=tytCQr3bNWOVqwFK/AprY7acK6lWfuLBya; SID=TwgxbA4bpxFTz6X3odu1d-6kRnHJ7M1O53f-22TbUxr7ABdJ2MaTLb8DMvh0EpJuF8GZcA.; __Secure-1PSID=TwgxbA4bpxFTz6X3odu1d-6kRnHJ7M1O53f-22TbUxr7ABdJyMI6eofeXwlkhd_VvP6nqQ.; __Secure-3PSID=TwgxbA4bpxFTz6X3odu1d-6kRnHJ7M1O53f-22TbUxr7ABdJj1rXp9sZdkxj-jk2Xdup6g.; NID=511=VWF3KQBBrdv8COzBjicSwLlA0UOjnHUtYuawd3CHsrdIPdIsIaNxUSLtA7Bk3oJw2nO34KISU59laVEvhPH1xzqkfCuh83EGO2nkeamf9T5lgWMsWqgDW5h8DfIZ7P4V44Iyljb_eK7cuNOoci1lC3a5HEdJ57-VSo856IOoEYkbHjc4Em6ruuXUU27XTnMiASqd-lz4H-ymaNvV__80h6sABK3JklfNYwGl5czJ_-h5ggmxw9yI4KABoYeB-hIjLHMlCsEenmaQuqOTZGDLPq9lrnlJpYyuDg0mAQ; 1P_JAR=2023-03-18-00; AEC=ARSKqsIpn7zbbBxzAssj9SdPe1pbUm50VOvrx7cVDnBL-PnYDGua0aOl2Q; OTZ=6946600_84_88_104280_84_446940; SIDCC=AFvIBn_Mn534oMno-Os9w-EER89PXHywi06O1HCrVHVb2NzKrGnzZOTuzXbons6tTiqXH2EL0KU; __Secure-1PSIDCC=AFvIBn9cenBQ_fe8MdG2jDTzIU-64aJN3x2wT9TvppjGfHb7taeDIoW4rW0BBSUJ0U4RANSejqg; __Secure-3PSIDCC=AFvIBn83eac8gyvahgw-Hudqew2hiOEK22Fmh7H37Gp-ueApMX5NAdfzkSNxXktKs1wfjnBVCzo"}},timeout=None, retries=3, backoff_factor=0.1)
category = "0"
location = ""
property = ""
timeframe = "today 5-y"
# testData2 = ["Poggers", "booba", "deez nuts", "monkas", "thicc", "cringe", "skinny legend", "brx", "bru", "leafy", "nightblue", "normie", "hello", "water"]

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_Slang(wordList):
    start_time = time.time()
    responses = await asyncio.gather(*[relatedSlang(kw) for kw in wordList])
    print("get_Slang --- %s seconds ---" % (time.time() - start_time))
    return list(filter(None, responses))


async def relatedSlang(keyword):
    
    slangTrend.build_payload([keyword], category, timeframe, location, gprop=property)
    data = slangTrend.related_queries()
    if data[keyword]["top"] is not None:
        relatedQueriesString = ' '.join(data[keyword]["top"]["query"].iloc[0:11])
        if "mean" in relatedQueriesString or "definition" in relatedQueriesString:
            return keyword
        return None 
    return None
