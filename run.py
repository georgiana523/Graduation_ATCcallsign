import Functions as sort_callsign
import pandas as pd
import re

df = (pd.read_csv("Digits.csv", encoding = "ISO-8859-1", usecols = ['Digit','Digit_word']))
digit_word = [_ for _ in df['Digit_word'].str.lower()]
digit = [_ for _ in df['Digit'].apply(str)]

def get_callsign(input_data):

    for i in range(len(input_data)):
        for index, item in enumerate(digit):
            if (input_data[i] == item):
                input_data = input_data.replace(str(item),str(digit_word[index])+" ")

    input_data = re.sub("[,~`^.?&%$!@]", '', input_data)
    input_data = input_data.lower()

    if ("flight level" in input_data):
        input_data = input_data.replace("flight level", "fl")
    if ("set course" in input_data):
        input_data = input_data.replace("set course", "setCourse")

    script_matched = sort_callsign.get_matches(input_data)
    delimiter = sort_callsign.delimiter(script_matched)

    #separate data at false matches
    sorted_data = []
    for idx, item in enumerate(script_matched):
        item = item.split()
        for i in range(1,len(delimiter)):
            new_line = ""
            for k in range(delimiter[i-1],delimiter[i]):
                new_line = new_line + item[k] + " "
            sorted_data.append(new_line)

    while ("" in sorted_data): 
        sorted_data.remove("") 

    separated_callsigns = sort_callsign.separate_callsigns(sorted_data)
    callsign_code = sort_callsign.get_callsign_code(separated_callsigns)

    callsign = []
    for item in callsign_code:
        if (len(item) >= 3):
            callsign.append(item)

    return callsign
