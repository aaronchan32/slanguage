import json

with open ("commonSlang.json", "r") as f:
    temp = json.load(f)

with open ("new.json", "w") as g:
    json.dump(temp, g, indent=4)
