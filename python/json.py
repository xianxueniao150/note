
import json

# Opening JSON file
f = open('he.json',)

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['data']['video_info']:
    print(i['title'],"      ",i['uname'])

# Closing file
f.close()
print("------------------------------------------------------      ")


for line in open("me.json"):
    if line.strip().startswith("\"title\"") or line.strip().startswith("\"uname\""):
        print(line.strip())


