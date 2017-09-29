import json
import random

#function for isolating the parameters that make a score descrete into +, neutral, -
def discretePosture(score):
    a = -0.05
    b = 0.05
    if -1 <= score < a:
        return -1 
    elif a <=score <= b :
        return  0
    elif b <= score <= 1:
        return 1 
    return None

#load data
with open("windows.json") as dataFile:
    data = json.load(dataFile)

#compute emoji ocurrences
emojiOcurrences = {}
top = -1
for tweet in data["tweets"]:
    for emoji in tweet["emojis"]:
        if emoji in emojiOcurrences:
            emojiOcurrences[emoji] += 1
            if emojiOcurrences[emoji] > top: top = emojiOcurrences[emoji]
        else:
            emojiOcurrences[emoji] = 1

#crearte tweet freq histogram
emojiChart = []
for key in emojiOcurrences:
    if int(emojiOcurrences[key]*100/top):
        emojiChart.append( [ key, ''.join(["█" for i in range(int(emojiOcurrences[key]*100/top))]) ] )
emojiChart = sorted(emojiChart, key=lambda x: len(x[1]), reverse=True)

print("Emoji ocurrences:")
for i in emojiChart:
    print(i[0], i[1])
print()

#compute tweets posture
postureOcurrence = {-1:0,0:0,1:0}
postureText = {-1:"Negative",0:"Neutral ",1:"Positive"}
top = -1
for tweet in data["tweets"]:
    score = discretePosture( (random.random()*2)-1 )#placeholder(tweet) #returns float form -1 to 1
    postureOcurrence[score] += 1 
    if postureOcurrence[score] > top: top = postureOcurrence[score] 

postureChart = []
for key in postureOcurrence:
    postureChart.append( [ key, ''.join(["█" for i in range(int(postureOcurrence[key]*100/top))]) ] )
postureChart = sorted(postureChart, key=lambda x: len(x[1]), reverse=True)

print("Posture ocurrences:")
for i in postureChart:
    print(postureText[i[0]], ":",  i[1])
