from sklearn.neural_network import MLPClassifier
import json
from pprint import pprint
import re

class emojiem:
    def __init__(self):
        #data loading
        self.emoji2vec = {}
        emotions2emoji = []

        with open("../emojis/emoji2vec.txt") as dataFile:    
            for line in dataFile:
                line = line.rstrip("\n")
                line = line.split(" ")
                self.emoji2vec[line[0]] = [float(i) for i in line[1:-1]]

        with open("../emojis/emotions.txt") as dataFile:    
            for line in dataFile:
                line = line.rstrip("\n")
                line = line.split(",")
                emotions2emoji.append(line)


        vec2emotions = [[self.emoji2vec[emoji], emotion] for emotion, emoji in emotions2emoji]


        trainingX = [i[0] for i in vec2emotions]
        trainingY = [i[1] for i in vec2emotions]

        #init and training neural network classifier with experimental paramters
        self.clf = MLPClassifier(solver='sgd', hidden_layer_sizes=(100,100,100,100,100,100), max_iter=100000)
        self.clf.fit(trainingX, trainingY)


    def evaluate(self, emojiArr):
        
        #normalized posture correspondance
        emotionScores = {"relajado":0.5, "tenso":-0.25, "alerta":0., "nervioso":-0.25, "emocionado":0.5, "estresado":-0.5, "exaltado":0.75, "decepcionado":-0.5, "feliz":1, "triste":-1, "satisfecho":0.75, "aburrido":-0.25, "fatigado":-0.25}
        #average emotional posture values per emoji in array using trained nn 
        n = 1
        result = 0
        for score in [emotionScores[res] for res in self.clf.predict([self.emoji2vec[em] for em in emojiArr])]:
            result += (score - result)/n
            n+=1
        return score

#results
#accuracy over training set
# accuracy = 1
# for el in [[icon, human, result] for icon, human, result in zip([emoji for _, emoji in emotions2emoji], [human for human, _ in emotions2emoji], clf.predict( [emoji2vec[emoji] for _, emoji in emotions2emoji]) )]:
#     if el[1] != el[2]:
#         accuracy -= 1/155



# print(accuracy)
# pprint(trainingSetResult)


# clustering
# clust = {emotion:[] for emotion, _ in emotions2emoji}
# for emoji in emoji2vec: 
#     clust[ clf.predict_proba([emoji2vec[emoji]])[0] ].append(emoji)

# for i in clust: print(i, sorted(clust[i]))