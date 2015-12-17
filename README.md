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
- 
## How to run the application.
There are two important steps to run the application. They are as follows:
- When running the application for the very first time, we need to calculate the TFDF first. In order to do that, you need have the raw data files ready inside **docs** folder. After that run the *generateTFIDF.py* code. This step is ONE TIME process only. If, the raw datase does not change, you need not re-run this again.
- The second and most important part is the json creation based on the user input. The user is asked to input two things. First, the word for which co-occcurance needs to be determined. And second, the number of layers the user wants to generate. This steps needs to executed everytime co-occurence for a new word is generated.

After the computations, we need to used visualization tools to see the application. For that Hierachie library has been used.  I am automatically generatting the JSON file and storing it in the required location. But if you move the visualization to a different location, the generated JSON file should be placed inside visualizaion/app/data folder. After that the index.html can be open by a localhost server.

##Understanding the Code
I have extensively commented the code in order to explain each step. In addition, I have also submitted the notebook file. Please refer these documents for further information.
