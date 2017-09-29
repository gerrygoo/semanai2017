import csv
import json
import unidecode
from difflib import SequenceMatcher
from emojiem import emojiem

csvfile = open('finalDictionary_Cabify.csv', 'r')

fieldnames = ("word","value")
reader = csv.DictReader(csvfile, fieldnames)

totDictionary = {}

for row in reader:
    totDictionary[unidecode.unidecode(row['word'])] = row['value']
    
# for element in totDictionary:
#     print(element)

def computeSimilarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getScore(similarity, foundWordScore):
    
    return similarity*foundWordScore
    
# Python program for insert and search
# operation in a Trie

# Taken from: http://www.geeksforgeeks.org/trie-insert-and-search/

ALPHABET_SIZE = 26
 
thing = emojiem()

class TrieNode:
     
    # Trie node class
    def __init__(self):
        self.children = [None]*ALPHABET_SIZE
 
        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
 
class Trie:
     
    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()
 
    def getNode(self):
     
        # Returns new trie node (initialized to NULLs)
        return TrieNode()
 
    def _charToIndex(self,ch):
         
        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
         
        return ord(ch)-ord('a')
     
    def _indexToChar(self,index):
        
        return chr(index + 97)
 
    def insert(self,key):
             
        # If not present, inserts key into trie
        # If the key is prefix of trie node, 
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
 
            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
 
        # mark last node as leaf
        pCrawl.isEndOfWord = True
 
    def search(self, key):
         
        # Search key in the trie
        # Returns true if key presents 
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        closestWord = ""
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
#                 print("closestWord = " + closestWord)
#                 return False 
                return closestWord
            pCrawl = pCrawl.children[index]
            closestWord += self._indexToChar(index)
     
#         print("closestWord = " + closestWord)
#         return pCrawl != None and pCrawl.isEndOfWord
        return closestWord

# Trie object
myTrie = Trie()

def computeTweetSentiment(tweetText):

	sentiment = 0
	wordCounter = 0

	for word in tweetText.split(" "):

		try:
			wordCounter = wordCounter + 1
			wordToSearch = word
			foundWord = myTrie.search(wordToSearch)
			# print("Wanted: " + wordToSearch)
			# print("Found: " + foundWord)

			similarity = computeSimilarity(wordToSearch, foundWord)
			# print("Similarity: " + str(similarity))
			# print("Found word's score = " + str(totDictionary[foundWord]))
			wordSentiment = getScore(similarity, float(totDictionary[foundWord]))
			# print("Desired word score: " + str(getScore(similarity, float(totDictionary[foundWord]))))
			sentiment = sentiment + wordSentiment

		except:
			pass

	return sentiment/wordCounter

def computeEmojisSentiment(tweetEmojiArray):

	return thing.evaluate(tweetEmojiArray)

def computePredominantSentiment(tweetEmojiArray):

	return thing.getPredominantEmotion(tweetEmojiArray)

def computeTotalSentiment(textScore, emojiScore):

	if abs(emojiScore) >= 0.70:
		return ((emojiScore*1.5) + textScore)/2

	return ((textScore*1.5) + emojiScore)/2

# driver function

def computeTweetObjectSentiment(tweet):
	return(computeTweetSentiment(tweet["full_text"]))

def main():

	originalTweetTextArray = []
	cleanTweetTextArray = []
	tweetEmojisArray = []

	jsonFile = open('cabify.json', 'r') 
	jsonArray = json.load(jsonFile)

	for element in totDictionary:
		myTrie.insert(element)

	for tweet in jsonArray['tweets']:

		originalTweetTextArray.append(tweet['fullTweet'])
		cleanTweetTextArray.append(tweet['full_text'])
		tweetEmojisArray.append(tweet['emojis'])

	for i in range(len(cleanTweetTextArray)):

		print("Original tweet text = " + originalTweetTextArray[i])
		print("Clean tweet text = " + cleanTweetTextArray[i])
		textScore = computeTweetSentiment(cleanTweetTextArray[i])
		print("Text score = " + str(textScore))

		if len(tweetEmojisArray[i]) > 0:
			emojiScore = computeEmojisSentiment(tweetEmojisArray[i])
			predominantSentiment = computePredominantSentiment(tweetEmojisArray[i])
			print("Emojis = " + str(tweetEmojisArray[i]))
			print("Emojis score = " + str(emojiScore))
			print("Emojis predominant sentiment = " + predominantSentiment)
			print("Total score = " + str(computeTotalSentiment(textScore, emojiScore)))

		else:
			print("This tweet did not have emojis.")

		print()

main()