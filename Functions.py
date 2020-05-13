import spacy
import pandas as pd

from spacy import displacy
nlp = spacy.load("en_core_web_lg")

from spacy.matcher import Matcher 
matcher = Matcher(nlp.vocab, validate = True)

from patterns_atc import create_patterns
matcher.add("PAT", None, *create_patterns())

numbers_pattern = [{'LIKE_NUM': True}]
matcher.add("NUM", None, numbers_pattern)

df = (pd.read_csv("List_of_airliners.csv", encoding = "ISO-8859-1", usecols = ['Airliner_code','Airliner_RT']))
airliner_rt = [_ for _ in df['Airliner_RT'].str.lower()]
airliner_code = [_ for _ in df['Airliner_code']]

df = (pd.read_csv("Phonetic_alphabet.csv", encoding = "ISO-8859-1", usecols = ['Symbol','Code_Word']))
phonetic_alphabet_code_word = [_ for _ in df['Code_Word'].str.lower()]
phonetic_alphabet_symbol = [_ for _ in df['Symbol']]

df = (pd.read_csv("Digits.csv", encoding = "ISO-8859-1", usecols = ['Digit','Digit_word']))
digit_word = [_ for _ in df['Digit_word'].str.lower()]
digit = [_ for _ in df['Digit'].apply(str)]

df = (pd.read_csv("False_Matches.csv", encoding = "ISO-8859-1", usecols = ['False_Matches']))
false_matches = [_ for _ in df['False_Matches']]

#get matched data with the spacy matcher
def get_matches(input_data):
    script_matched = [] 
    matched_words = ""
    doc = nlp(input_data)
    for idx, start, end in matcher(doc):
        matched_words = matched_words + " " + str(doc[start: end].text)
    script_matched.append(matched_words)

    if (script_matched[0] == " "):
        script_matched = script_matched[1:]

    return script_matched

#get index of false matches(such as flight level, taxiing)
#from the matched data
def delimiter(script_matched):
    delimiter = [0]

    for idx, item in enumerate(script_matched):
        item = item.split()
        total_length = len(item)
        three_words_callsign = ""
        two_words_callsign = ""
        for index in range(2,len(item)):
            if (item[index][0] == " "):
                item[index] = item[index][1:]
            if (item[index][-1] == " "):
                item[index] = item[index][:-1]
            three_words_airliner = item[index-2] + " " + item[index-1] + " " + item[index]
            two_words_airliner = item[index-2] + " " + item[index-1]
            for airliner in airliner_rt:
                if (airliner[0] == " "):
                    airliner = airliner[1:]
                if (airliner[-1] == " "):
                    airliner = airliner[:-1]
                if (airliner == item[0]):
                    delimiter.append(0)
                if (airliner == item[1]):
                    delimiter.append(1)
                if (airliner == three_words_airliner ):
                    delimiter.append(index-2)
                if (airliner == two_words_airliner):
                    delimiter.append(index-2)
                if (airliner == item[index]):
                    delimiter.append(index)
            for false_match in false_matches:
                if (false_match == item[index]):
                    delimiter.append(index)

    delimiter.append(total_length)
    delimiter = list(dict.fromkeys(delimiter))

    return delimiter

#distinguish between general aviation callsigns and airliners
def separate_callsigns(sorted_data):
    split_item = ""
    new_item = ""
    f = ""
    check_letters = 0
    is_general_aviation = False
    for j in range(len(sorted_data)):
        data_item = sorted_data[j].split()
        for idx in range(len(data_item)):
            for alphabet_code_word in phonetic_alphabet_code_word:
                if (alphabet_code_word in data_item[idx]):
                    check_letters += 1
            if (check_letters == len(data_item)-1):
                is_general_aviation = True

    if (is_general_aviation == False):
        for j in range(len(sorted_data)):
            for idx in range(len(data_item)):
                for alphabet_code_word in phonetic_alphabet_code_word:
                    if (alphabet_code_word in sorted_data[j]):
                        nr =0
                        data_item =sorted_data[j].split()
                        for index in range(2, len(data_item)):
                            for alphabet_code_word1 in phonetic_alphabet_code_word:
                                if (data_item[index-2] == alphabet_code_word1):
                                    for alphabet_code_word2 in phonetic_alphabet_code_word:
                                        if (data_item[index-1] == alphabet_code_word2):
                                            for alphabet_code_word3 in phonetic_alphabet_code_word:
                                                if (data_item[index] == alphabet_code_word3):
                                                    split_item = ' '.join(sorted_data[j].split(str(data_item[index-2]))[1:])
                                                    new_item = str(data_item[index-2]) + split_item
                                                    sorted_data.insert(j+1,new_item)
                sorted_data = list(dict.fromkeys(sorted_data))

    for j in range(len(sorted_data)):
        for false_match in false_matches:
            if (false_match in sorted_data[j]):
                sorted_data[j] = ""
    
    return sorted_data

#convert the data sorted to the corresponding codes
def get_callsign_code(separated_callsigns):
    callsign_code = []
    new_callsign_code = ""
    military_callsign = ""
    two_words_callsign = ""
    military = ""
    is_military_callsign = False

    for item in separated_callsigns:
        callsign_code.append(new_callsign_code)
        item_split = item.split()
        new_callsign_code = ""
        if "air force" in item:
            is_military_callsign = True

        for j in range(len(item_split)):
            if (j <= len(item_split)-2):
                two_words_callsign = str(item_split[j]) + " " + str(item_split[j+1])
            if (is_military_callsign == True):
                military_callsign = ""
                military = item_split[j:j+3]

            for k in range(len(military)):
                military_callsign = military_callsign + str(military[k]) + " "
            military_callsign = military_callsign[:-1]

            for index, airliner in enumerate(airliner_rt): 
                if (airliner[-1] == " "):
                    airliner = airliner[:-1]
                if (airliner[0] == " "):
                    airliner = airliner[1:]
                if (two_words_callsign == airliner):
                    new_callsign_code += str(airliner_code[index])
                    two_words_callsign = ""
                if (item_split[j] == airliner):
                    new_callsign_code += str(airliner_code[index])
                elif (military_callsign == airliner):
                    new_callsign_code += str(airliner_code[index])
                    is_military_callsign = False

            for index, alphabet_code_word in enumerate(phonetic_alphabet_code_word):
                if (item_split[j] == alphabet_code_word):
                    new_callsign_code += str(phonetic_alphabet_symbol[index])

            for index, number in enumerate(digit_word):  
                if (item_split[j] == number):
                    new_callsign_code += str(digit[index])  
        new_callsign_code = new_callsign_code.replace(" ","")
        callsign_code.append(new_callsign_code)
 
    callsign_code = list(dict.fromkeys(callsign_code))

    return callsign_code
