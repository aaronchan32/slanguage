import requests, aiohttp, asyncio, time, json, string
from datetime import date
from collections import ChainMap

currentDate = date.today()

dummyList = ['have','the','banana', 'yeehaw', 'sus', '?', 'a', 'asdikuifg', 'poggers']

start_time = time.time()

def getMeaning(file):
    meaning = file["list"][0]["definition"]
    meaning = meaning.replace("[", "").replace("]", "").capitalize()
    return meaning


def getUpvotes(file):
    upvotes = str(file["list"][0]["thumbs_up"])
    return upvotes

# def getDownvotes(file):
#     downvotes = str(file["list"][0]["thumbs_down"])
#     return downvotes


# def getUploadDate(file):
#     uploadYr = file["list"][0]["written_on"][0: 10]
#     return uploadYr

# def getSlang(myDict):
#     slangDict = {}
#     for word in myDict:
#         url = "http://api.urbandictionary.com/v0/define?term={}".format(word)
#         response = requests.get(url)
#         if response.ok:
#             file = response.json()
#             # if int(getUploadDate(file)[0: 4]) > currentDate.year - 10:
#             if len(file["list"]) != 0:
#                 slangDict[word] = {
#                     "Meaning": getMeaning(file),
#                     "Upvotes": getUpvotes(file),
#                     "Downvotes": getDownvotes(file),
#                     "UploadDate": getUploadDate(file),
#                     "URL": "https://www.urbandictionary.com/define.php?term={}".format(word)
#                 }
#     return slangDict

mostCommonWordsSet = set(line.strip() for line in open ('mostCommonWords.txt'))
f = open ('commonSlang.json', "r")
commonSlangJson = json.loads(f.read())
    

def commonFilter(json):
    start_time = time.time()
    slangDict = {}
    finalSlang = []
    tempSlang = []
    for message in reversed(json["messages"]):
            if "content" in message:
                words = message["content"].split()
                for word in words:
                    punctuatedWord = word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '')
                    if word in commonSlangJson:
                        finalSlang.append(word)
                        continue
                    if punctuatedWord in commonSlangJson:
                        finalSlang.append(punctuatedWord)
                        continue
                    if len(punctuatedWord) > 2:
                        if (punctuatedWord[-1] == 's' or punctuatedWord[-1] == 'd') and (punctuatedWord[0:-1] in mostCommonWordsSet):
                            continue
                        if (punctuatedWord[-2:] == 'nt' or punctuatedWord[-2:] == 've' or punctuatedWord[-2:] == 're' or punctuatedWord[-2:] == 'er' or punctuatedWord[-2:] == 'ly' or punctuatedWord[-2:] == 'ed') and (punctuatedWord[0:-3] in mostCommonWordsSet or punctuatedWord[0:-2] in mostCommonWordsSet) or punctuatedWord[0:-1] in mostCommonWordsSet:
                            continue
                        if (punctuatedWord not in mostCommonWordsSet) and len(word) < 50:
                            tempSlang.append(punctuatedWord)
                            continue


    slangDict["finalSlang"] = list(set(finalSlang))
    slangDict["tempSlang"] = list(set(asyncio.run(initialUrbanFilter(tempSlang))))
    print("commonFilter --- %s seconds ---" % (time.time() - start_time))
    return slangDict
                    
async def finalUrbanFilter(finalList, tempList): 
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        tasks = []
        for word in finalList:
            task1 = asyncio.ensure_future(getWordDataFinal(session, word))
            tasks.append(task1)
        
        for word in tempList:
            task2 = asyncio.ensure_future(getWordDataTemp(session, word))
            tasks.append(task2)

        slangDict = await asyncio.gather(*tasks)
        slangArray = list(filter(None, slangDict))
        
        slangDict = dict(ChainMap(*slangArray))
        print("urbanFilter --- %s seconds ---" % (time.time() - start_time))
        return slangDict


async def getWordDataTemp(session, word):
    slangDict = {}
    url = "http://api.urbandictionary.com/v0/define?term={}".format(word)

    async with session.get(url) as response:
        file = await response.json()
        if response.status == 200:
            if file["list"] != [] and int(getUpvotes(file)) > 100:
                slangDict[word] = getMeaning(file)
                return slangDict
        else:
            return {}

async def getWordDataFinal(session, word):
    slangDict = {}
    url = "http://api.urbandictionary.com/v0/define?term={}".format(word)

    async with session.get(url) as response:
        file = await response.json()
        if response.status == 200:
            if file["list"] != []:
                slangDict[word] = getMeaning(file)
                return slangDict
        else:
            return {}

async def initialUrbanFilter (tempList):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        slangList = await asyncio.gather(*[initialFilter(session, word) for word in tempList])
        filteredList = list(filter(None, slangList))
        
        
        print("urbanFilter --- %s seconds ---" % (time.time() - start_time))
        return filteredList

async def initialFilter (session, word):
    url = "http://api.urbandictionary.com/v0/define?term={}".format(word)

    async with session.get(url) as response:
        file = await response.json()
        if response.status == 200:
            if file["list"] != [] and int(getUpvotes(file)) > 100:
                return word
        else:
            return ''


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# print(asyncio.run(main(commonFilter(dummyData))))
# print("--- %s seconds ---" % (time.time() - start_time))

