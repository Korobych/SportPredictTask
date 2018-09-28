#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests

# Today
class Parser:
   
    def __init__(self):
        self.url = "https://www.myscore.ru/"
    def GetUrl(self,url=0):
        if url==0:    
            res = requests.get(self.url)
            return res.text
        else:
            res = requests.get(url)
            return res.text
    
    # Friday Task
    def Today(self):
        page = self.GetUrl() #  == res.text
        soup = BeautifulSoup(page,"html.parser")
        check = soup.find("div",{"id":"fscon"})
        print(check)
    
if __name__=="__main__":
    full = Parser()
    full.Today()
        

    
