# Graduation_ATCcallsign

This project contains a prototype to generate atc callsigns. The code is written in python and the SpaCy library is used. The SpaCy library needs to be installed to run this code.

This is not a trained nlp model. The SpaCy matcher is used to identify certain sets of words, which are then converted into a callsign format.

This is an amateur Python project.

This prototype cannot be used for operational purpose.

Automated generation of SpaCy patterns                                                                                          
-By running "sort_patterns.py", all the patterns are created in "patterns_atc.py".                                                           
-The patterns are in spaCy format and they contain the airliner designators and the phonetic alphabet code words.                 
-In "patterns_atc_callsign.py" the funtion "create_patterns()".                                                          
-To use it, "create_patterns()" needs to be imported in the run file.                                                          

The run file                                                                                                                                                                              
-The patterns generetared are imported and added to the spaCy matcher.                                                          
-The numbers pattern that spaCy provides is added to the matcher as well.                                                          
-The functions used to sort the data are imported from "Functions.py".                                                          
