__author__ = 'mrtyormaa'

from nltk.compat import raw_input
from scipy.io import mmread
import operator
import json
from gensim import corpora
import logging

#
# This is for logging data
#
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('text_mining_logger')

# Pre-processing steps required to load the Dictionary and TFIDF
# Retrieve the dictionary
#
logger.info("Loading the dictionary.")
dictionary = corpora.Dictionary.load('files/pubMed-dictionary.dict')

#
# Let's tokenize the dictionary and get the word <-> id pairs.
#
id2word = dictionary.token2id

#
# inverse dictionary. This is easy for future lookups of ids
#
word2id = {val: key for key, val in id2word.items()}

#
# Retrieve the TFIDF
#
logger.info("Loading the TFIDF.")
file = mmread('files/pubMed-tfidf.mm')

#
# User input
#
print("Enter a word for which you want co-occurance: ")
user_word = raw_input()
print("How many layers of output do you want to generate(0-5): ")
level = int(raw_input())


#
# This method returns all the documents containing the given word.
#
def getDocumentsWithParam(param):
    docs = []
    id = id2word[param]
    i = 0
    for col in file.col:
        if col == id:
            docs.append(file.row[i])
        i += 1
    return docs


#
# This method returns all the words in the document.
#
def getWordsAndTFIDF(docId):
    data = []
    i = 0
    for row in file.row:
        if docId == row:
            data.append([file.col[i], file.data[i]])
        i += 1
    return data


#
# This is a recursive method used to generate the relevant words
#
def generateRelevantWords(param, l):
    docs = getDocumentsWithParam(param)
    relevant_words = {}
    for doc in docs:
        data = getWordsAndTFIDF(doc)
        for d in data:
            #
            # Ignore already visited words. This is to avoid repetition of words.
            #
            if word2id[d[0]] in visited_words:
                continue
            if not d[0] in relevant_words:
                relevant_words[d[0]] = 0.0
            relevant_words[d[0]] += d[1]
    #
    # One of the base cases of recursion. If we don't find relevant words, return null array.
    #
    if not relevant_words:
        return []
    #
    # We sort the words in decreasing order of their TFIDF values. This gives us tuples of
    # word and tfidf. (word, tfidf)
    #
    word_tfidf_tuples = sorted(relevant_words.items(), key=operator.itemgetter(1), reverse=True)

    #
    # Let's limit the relevant words to 5 for each word.
    #
    word_tfidf_tuples = word_tfidf_tuples[0:5]

    for word in word_tfidf_tuples:
        visited_words.append(word2id[word[0]])
    tree = []

    for word in word_tfidf_tuples:
        current_word = []
        current_word.append(word2id[word[0]])
        topic = {}
        topic['words'] = current_word
        topic['name'] = 'Topic_0'
        if (l == level - 1):
            tree.append(topic)
        else:
            #
            # Go another deeper level.
            #
            result = generateRelevantWords(word2id[word[0]], l + 1)
            if result:
                topic['children'] = result
            tree.append(topic)
    return tree


json_response = {}
visited_words = []
visited_words.append(user_word)
json_response['name'] = user_word
json_response['words'] = [user_word]

logger.info("Generating the Relevant Words.")
json_response['children'] = generateRelevantWords(user_word, 0)

logger.info("Saving the JSON file.")
with open('/Users/mrtyormaa/Sites/Hierarchie/app/data/pub-med.json', 'w') as outfile:
    json.dump(json_response, outfile)
