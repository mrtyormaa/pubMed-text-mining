__author__ = 'mrtyormaa'

#
# Imports
#
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
word_to_id = dictionary.token2id

#
# inverse dictionary. This is easy for future lookups of ids
#
id_to_word = {val: key for key, val in word_to_id.items()}

#
# Retrieve the TFIDF
#
logger.info("Loading the TFIDF.")
tfidf_matrix = mmread('files/pubMed-tfidf.mm')

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
    id = word_to_id[param]
    i = 0
    for col in tfidf_matrix.col:
        if col == id:
            docs.append(tfidf_matrix.row[i])
        i += 1
    return docs

#
# This method returns all the words in the document.
#
def getWordsAndTFIDF(docId):
    word_list_per_document = []
    i = 0
    for row in tfidf_matrix.row:
        if docId == row:
            word_list_per_document.append([tfidf_matrix.col[i], tfidf_matrix.data[i]])
        i =i + 1
    return word_list_per_document

#
# This is a recursive method used to generate the relevant words
#
def generateRelevantWords(param, lev):
    docs = getDocumentsWithParam(param)
    relevant_words = {}
    for doc in docs:
        data = getWordsAndTFIDF(doc)
        for dat in data:
            #
            # Ignore already visited words. This is to avoid repetition of words.
            #
            if id_to_word[dat[0]] in visited_words:
                continue
            if not dat[0] in relevant_words:
                relevant_words[dat[0]] = 0.0
            relevant_words[dat[0]] += dat[1]
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
        visited_words.append(id_to_word[word[0]])
    tree = []

    for word in word_tfidf_tuples:
        current_word = []
        current_word.append(id_to_word[word[0]])
        topic = {}
        topic['words'] = current_word
        topic['name'] = 'Topic_0'
        if (lev == level - 1):
            tree.append(topic)
        else:
            #
            # Go another deeper level.
            #
            result = generateRelevantWords(id_to_word[word[0]], lev + 1)
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
