import spacy
import pandas as pd

from spacy import displacy
nlp = spacy.load("en_core_web_lg")

from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab, validate = True)

df = (pd.read_csv("Phonetic_alphabet.csv", encoding = "ISO-8859-1", usecols = ['Code_Word']))
phonetic_alphabet_code_word = [_ for _ in df['Code_Word'].str.lower()]

df = (pd.read_csv("List_of_airliners.csv", encoding = "ISO-8859-1", usecols = ['Airliner_RT']))
airliner_rt = [_ for _ in df['Airliner_RT'].str.lower()]

df = (pd.read_csv("False_Matches.csv", encoding = "ISO-8859-1", usecols = ['False_Matches']))
false_matches = [_ for _ in df['False_Matches']]

result_file = open("patterns_atc.py", "w")
n = result_file.write("def create_patterns():\n	patterns_atc = [ \n")

for index, item in enumerate(phonetic_alphabet_code_word):
    if '-'  in item:
        x_1 = item.index('-')
        y_2 = "		[{'LOWER':\""  + item[:x_1] + "\"}, {'IS_PUNCT': True, 'OP':'?'}, {'LOWER': '" + item[x_1+1:]  + "'}],\n"
    else:
        y_2 = "		[{'LOWER':\""  + item + "\"}],\n"
    n = result_file.write(y_2)

for index, item in enumerate(false_matches):
    if " " in item:
        x_2 = item.index(" ") 
        y_2  = "		[{'LOWER':\""  + item[:x_2] + "\"}, {'LOWER':\"" + item[x_2+1:] + "\"}],\n"
    else:	
        y_2 = "		[{'LOWER':\""  + item + "\"}],\n"
    n = result_file.write(y_2)

for index, item in enumerate(airliner_rt):
    if item[0] == " ":
        item = item[1:]
    if item[-1] == " ":
        item = item[:-1]
    if '-'  in item:
        x_3 = item.index('-')
        y_3 = "		[{'LOWER':\" "  + item[:x_3] + "\"}, {'IS_PUNCT': True, 'OP':'?'}, {'LOWER': '" + item[x_3+1:]  + "'}],\n"
    elif (item == "level"):
        y_3 = "		[{'LOWER':\""  + item + "\", 'POS': {'IN': ['PROPN']}}],\n"
    elif " " in item:
        x_3 = item.index(" ")
        item_new = item[x_3+1:]
        if " " in item_new:
            y_4 = item_new.index(" ")
            item_new2 = item_new[y_4+1:] 
            if " " in item_new2:
                y_5 = item_new.index(" ")
                y_3  = "		[{'LOWER':\""  + item[:x_3] + "\"}, {'LOWER':\"" + item_new[:y_4] + "\"}, {'LOWER':\"" + item_new2[y_5+1:] + "\"}],\n"
            elif '-'  in item:
                y_6 = item.index('-')
                y_3 = "		[{'LOWER':\""  + item[:x_3] + "\"}, {'LOWER':\"" + item_new[:y_4] + "\"}, {'LOWER': '" + item_new2[y_6+1:]  + "'}],\n"
            else:
                y_3  = "		[{'LOWER':\""  + item[:x_3] + "\"}, {'LOWER':\"" + item_new[:y_4] + "\"}, {'LOWER':\"" + item_new[y_4+1:] + "\"}],\n"
        elif '-'  in item:
            z = item.index('-')
            y_3 = "		[{'LOWER':\" "  + item[:z] + "\"}, {'IS_PUNCT': True, 'OP':'?'}, {'LOWER': '" + item[z+1:]  + "'}],\n"
        else:
            y_3  = "		[{'LOWER':\""  + item[:x_3] + "\"}, {'LOWER':\"" + item[x_3+1:] + "\"}],\n"
    else:	
        y_3 = "		[{'LOWER':\""  + item + "\"}],\n"
    n = result_file.write(y_3)

n = result_file.write("	] \n	return patterns_atc \n")
result_file.close()

