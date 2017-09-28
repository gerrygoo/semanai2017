from sklearn.neural_network import MLPClassifier
import json
from pprint import pprint
import re

#data load
emoji2vec = {}
emotions2emoji = []
spacep = re.compile("\s+", re.MULTILINE)

with open("../emojis/emoji2vec.txt") as dataFile:    
    for line in dataFile:
        line = line.rstrip("\n")
        line = line.split(" ")
        emoji2vec[line[0]] = [float(i) for i in line[1:-1]]

with open("../emojis/emotions.txt") as dataFile:    
     for line in dataFile:
        line = line.rstrip("\n")
        line = line.split(",")
        emotions2emoji.append(line)


vec2emotions = []
for emotion, emoji in emotions2emoji:
    vec2emotions.append([emoji2vec[emoji], emotion])

trainingX = [i[0] for i in vec2emotions]
trainingY = [i[1] for i in vec2emotions]

#training classifier
vbose = False
clf = MLPClassifier(solver='sgd', hidden_layer_sizes=(100,100,100,100,100,100), max_iter=100000, verbose = vbose)
clf.fit(trainingX, trainingY)

#results
#accuracy over training set
accuracy = 1
for el in [[icon, human, result] for icon, human, result in zip([emoji for _, emoji in emotions2emoji], [human for human, _ in emotions2emoji], clf.predict( [emoji2vec[emoji] for _, emoji in emotions2emoji]) )]:
    if el[1] != el[2]:
        accuracy -= 1/155



print(accuracy)
# pprint(trainingSetResult)


#clustering
# clust = {emotion:[] for emotion, _ in emotions2emoji}
# for emoji in emoji2vec: 
#     clust[ clf.predict([emoji2vec[emoji]])[0] ].append(emoji)

# for i in clust: print(i, sorted(clust[i]))