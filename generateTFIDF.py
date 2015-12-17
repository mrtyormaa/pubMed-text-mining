__author__ = 'mrtyormaa'

#
# Imports
#
from gensim import corpora
from gensim.corpora import MmCorpus
from gensim.models import TfidfModel
import glob
import os
import re
import logging

#
# This is for logging data
#
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('text_mining_logger')

#
# We will be appending all our documents to this array.
#
documents = []

#
# get the class-names from the directory structure
#
directory_names = list(set(glob.glob(os.path.join("docs", "*"))
                           ).difference(set(glob.glob(os.path.join("docs", "*.*")))))
#
# List of string of class names
#
namesClasses = list()

#
# Navigate through the list of directories recursively
#
logger.info("Reading the documents")
for folder in directory_names:
    #
    # Append the string class name for each class
    #
    currentClass = folder.split(os.pathsep)[-1]
    namesClasses.append(currentClass)

    for fileNameDir in os.walk(folder):
        for fileName in fileNameDir[2]:
            #
            # Only read in the text files
            #
            if fileName[-4:] != ".txt":
                continue
            nameFileImage = "{0}{1}{2}".format(fileNameDir[0], os.sep, fileName)
            with open(nameFileImage, 'r') as myfile:
                #
                # Read the file and remove the new-line characters.
                #
                data=myfile.read().replace('\n', '')
                #
                # Remove all special characters.
                #
                new_string = re.sub('[^a-zA-Z0-9]', ' ', data)
            documents.append(new_string)

#
# Remove common words and tokenize
#
logger.info("Pre-processing the documents to remove common words.")
stoplist = set('for a an of the and to in is are when what how where ha etc et all'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
      for document in documents]
#
# remove words that appear only once
#
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
 for token in text:
     frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
      for text in texts]

#
# We create a dictionary so that we don't have to deal with strings.
# Working with strings is very expensive. Instead we will be representing each word
# by a id and we will maintaining the mapping of the word <-> id in our dictionary
#
dictionary = corpora.Dictionary(texts)

#
# store the dictionary, for future reference
#
logger.info("Saving Dictionary.")
dictionary.save('files/pubMed-dictionary.dict')

#
# Generate tge dictionary for word id pair.
#
id_to_word = dictionary.token2id

corpus = [dictionary.doc2bow(text) for text in texts]

#
# Store to disk, for later use.
#
logger.info("Saving the corpus.")
corpora.MmCorpus.serialize('files/pubMed-corpus.mm', corpus)

#
# Load the corpus.
#
corpus_matrix = MmCorpus('files/pubMed-corpus.mm')

logger.info("Computing the TFIDF Matrix.")
tfidf = TfidfModel(corpus_matrix, id2word=id_to_word, dictionary=dictionary, normalize=True)

#
# Store the TF-IDF so that we don't have to calculate it every time.
#
logger.info("Saving the TFIDF.")
MmCorpus.serialize('files/pubMed-tfidf.mm', tfidf[corpus_matrix], progress_cnt=10000)
