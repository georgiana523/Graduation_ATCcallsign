import spacy
import pandas as pd

from spacy import displacy
nlp = spacy.load("en_core_web_lg")

from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab, validate=True)

df = (pd.read_csv("fullData.csv", encoding = "ISO-8859-1", usecols = ['transcription']))
scripts = [_ for _ in df['transcription'].str.lower()]

#run sort.py
from patterns_atc import create_patterns
matcher.add("PAT", None, *create_patterns())

numbers_pattern = [{'LIKE_NUM': True}]
matcher.add("NUM", None, numbers_pattern)

result_file = open("train_data.py", "w")
m = result_file.write("def create_trainingData():\n	TRAIN_DATA = [ \n")

def parse_train_data(doc):
	detections = [(doc[start:end].start_char, doc[start:end].end_char, 'CALL_S') for idx, start, end in matcher(doc)]
	a = (doc.text, {'entities': detections})
	b = str(a) + ","
	return b

for script in scripts:
    y = parse_train_data(nlp(script))
    m = result_file.write("		" + str(y) + "\n")

m = result_file.write("	] \n	return TRAIN_DATA \n")
result_file.close()
