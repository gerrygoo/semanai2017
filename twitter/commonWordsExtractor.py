import json
import nltk
import unidecode
from nltk.corpus import stopwords

def getStopWords():

    totalSpanishStopWords = stopwords.words('spanish')
    fixedTotalSpanishStopWords = []
    # no accents

    for word in totalSpanishStopWords:
        fixedTotalSpanishStopWords.append(unidecode.unidecode(word))

    return fixedTotalSpanishStopWords
	
totalSpanishStopWords = getStopWords()
# print(totalSpanishStopWords)

def readJSONFile(fileName):

	file = open(fileName, 'r') 
	jsonArray = json.load(file)
	return jsonArray

def getTweetArray(jsonArray):
	
	tweetArray = []

	for tweet in jsonArray['tweets']:
		tweetArray.append(tweet['full_text'])

	return tweetArray

def isWord(w):

	return w.isalpha()

def isStopWord(w):

	for sw in totalSpanishStopWords:
		if w == sw:
			return True

	return False

def comesFromBaseWord(totWordsMap, w):

	for word in totWordsMap:
		if w.startswith(word):
			return True

	return False

def getTweetWordMap(tweetArray):

	totWordsMap = {}

	for tweet in tweetArray:
		
		totWords = tweet.split(" ")

		for word in totWords:

			if len(word) <= 3 or isWord(word) == False or isStopWord(word) or comesFromBaseWord(totWordsMap, word):
				continue

			if word not in totWordsMap:
				totWordsMap[word] = 1
			
			else:
				totWordsMap[word] += 1

	return totWordsMap

def getTweetPopularWordsSet(totWordsMap, desiredAmount):

	return sorted(totWordsMap, key = lambda x : totWordsMap[x], reverse = True)[:desiredAmount]


def createOutputFile(popularWordsSet, outputFileName):

	file = open(outputFileName, 'w')

	for w in popularWordsSet:
	    file.write(w + ",")

	file.close()

def main():

	fileName = "cabify3000.json"
	desiredAmount = 150
	outputFileName = "cabify" + str(desiredAmount) + "MostCommonWords.txt"
	jsonArray = readJSONFile(fileName)
	tweetArray = getTweetArray(jsonArray)
	totWordsMap = getTweetWordMap(tweetArray)
	popularWordsSet = getTweetPopularWordsSet(totWordsMap, desiredAmount)
	createOutputFile(popularWordsSet, outputFileName)

main()