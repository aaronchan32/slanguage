import json

wordList = ["bananwafer", "bubberducky", "erenchen"]
newList = {}
for word in wordList:
    newList[word.strip()] = ''
with open('commonSlangcopy.json', 'r+') as file:
    data = json.load(file)
    data.update(newList)
    file.seek(0)
    json.dump(data, file)

        





#do some has_key() stuffs later






