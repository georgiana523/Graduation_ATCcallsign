import pytest
import run as nlpModel

@pytest.fixture
def text():
    x_0 = "lufthansa five three one eight  zurich klm one three four alpha bravo decimal six contact zurich alfa zero transavia one three four alfa bravo"
    x_1 = "hapag lloyd six five three climb flight level two nine zero set course trasadingen "
    x_2 = "alitalia station co= ah alitalia four eight seven i got it you're identified "
    x_3 = "belgian airforce four four is identified "
    x_4 = "german air force five eight five rhein radar identified "
    x_5 = "foxtrot sierra india climb flight level three one zero "
    x_6 = "rotterdam jetcenter six eight six report heading "
    x_7 = "air kuban eight two one four six alfa bravo climb to flight level two nine zero maintain present heading"
    x_8 = " air malta zero zero four rhein radar identified, netherlands air force one four rhein radar identified  "
    x_9  = "india oscar kilo call rhein on one two seven three seven good day  "
    x_10 = "hotel bravo india tango romeo is identified expect higher in a minute i'll call you back "
    return [x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10]

def test_method0(text):
    x_0 = ['DLH5318', 'KLM134AB', 'TRA134AB']
    assert nlpModel.get_callsign(text[0]) ==  x_0

def test_method1(text):
    x_1 = ["HLF653"]
    assert nlpModel.get_callsign(text[1]) ==  x_1

def test_method2(text):
    x_2 = ["AZA","AZA487"]
    assert nlpModel.get_callsign(text[2]) ==  x_2

def test_method3(text):
    x_3 = ["BAF44"]
    assert nlpModel.get_callsign(text[3]) ==  x_3

def test_method4(text):
    x_4 = ["GAF585"]
    assert nlpModel.get_callsign(text[4]) ==  x_4

def test_method5(text):
    x_5 = ["FSI"]
    assert nlpModel.get_callsign(text[5]) ==  x_5

def test_method6(text):
    x_6 = ["JCR686"]
    assert nlpModel.get_callsign(text[6]) ==  x_6

def test_method7(text):
    x_7 = ["KIL82146AB"]
    assert nlpModel.get_callsign(text[7]) ==  x_7

def test_method8(text):
    x_8 = ["AMC004", "NAF14"]
    assert nlpModel.get_callsign(text[8]) ==  x_8

def test_method9(text):
    x_9 = ["IOK"]
    assert nlpModel.get_callsign(text[9]) ==  x_9

def test_method10(text):
    x_10 = ["HBITR"]
    assert nlpModel.get_callsign(text[10]) ==  x_10
