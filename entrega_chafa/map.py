import re
import json
from pprint import pprint

#TODO leer json de tweets
#histograma de emociones de tweets
#histograma de emojis totales

def emojiEval(string):

    #emoji part
    with open("em.json") as dataFile:
        emoMap = json.load(dataFile)
    headers = [
        "score",
        "relajado",
        "tenso",
        "alerta",
        "nervioso",
        "emocionado",
        "estresado",
        "exaltado",
        "decepcionado",
        "feliz",
        "triste",
        "satisfecho",
        "aburrido",
        "fatigado"
    ]
    reg = re.compile("(" +"|".join(sorted([key for key in emoMap])) + ")")

    match = reg.findall(string)
    if match:
        generalScores = {}
        for i in headers: generalScores[i] = 0

        n = 1
        for emoji in match:

            emojiScores = emoMap[emoji]


            for i, param in enumerate(headers):
                old = generalScores[param]
                generalScores[param] += (emojiScores[i] - generalScores[param])/n
            n += 1


        
    else: return None

    return generalScores

def esEval(string):
    #spanish part
    with open("esp.json") as dataFile:
        # dictionary = {el["población"]:el["-0.2"] for el in json.load(dataFile)}
        for el in json.load(dataFile):
            pprint(el['-0.2'])

    
    score = 0
    # reg = re.compile("(" +"|".join(sorted([key for key in emoMap])) + ")")
    n = 1
    for word in string.split(" "):
        if word in dictionary:

            score += (dictionary[word] - score)/n


    return score

while 1:
    pprint(esEval(input(">")))
