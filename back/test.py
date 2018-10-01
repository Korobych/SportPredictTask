import parser
from random import choice
import asyncio
import time

def Test():
    parserCheck = parser.Parser()
    nice = 0
    bad = 0
    for i in range(30):
        lenOfFrame =  parserCheck.Today()
        if lenOfFrame == 0:
            print("bad")
            bad+=1
            time.sleep(2)
        else:
            print("nice")
            nice+=1
            time.sleep(2)
    print("Nice:"+str(nice)+";Bad:"+str(bad))
    
Test()