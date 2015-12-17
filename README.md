# pubMed-text-mining
## Directory Structure
This project contains 2 main components
- Python Files: These files are used to generate the JSON document containing the co-occuring words.
  - generateTFIDF.py: This file creates the TFIDF and Dictionary which will be used later on to generate the relevant words.
  - generateRelevantWords.py: This file uses the TFIDF and creates a json file which can be used by the visualization application (as discusssed later) to create a visualization of words.
- Visualization Files: These files create a web-application for visualization of the words. The files can be found under **visualization** folder.
  - Live Demo: Please visit [http://asutosh-satapathy.com/](http://asutosh-satapathy.com/) for a live demo of the application.
- Raw Data: The raw data can be put inside the **docs** folder. The application recursiveely traverses through all .txt files inside the doc folder. In order to save space, I have uploaded a few of dataset files.
- Additonal Files: The application generates a few temporary files which are used for computation. For example, the Doctionary and TFIDF Matrix files are saved. These files are stored inside **files** folder.
