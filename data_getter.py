from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
from selenium.webdriver.common.keys import Keys
from operator import itemgetter


with open('ourmodel.json', 'rb') as fout:
    data = json.load(fout)

res = {}

for i in data:
    res.update(i)


driver = webdriver.Chrome("./chromedriver")
driver.get("https://research.google.com/semantris/")

time.sleep(15)

driver.execute_script("this.game.audio.setMuted()")

wordlist = []
words = []
index = 0

target_index = 0


while True:

    TARGET = []
    while len(TARGET) == 0:  
        TARGET =  driver.execute_script("return this.game.currentGame.targetLines")

    
    print("target", TARGET)

    full = []
    for i in TARGET:
        full += res[i]

    words = sorted(full, key=itemgetter('score'), reverse=True)

    
    for word in words:
        bestMatch = word['word']
        banned_prefixes = driver.execute_script("return this.game.currentGame.bannedPrefixes")
        banned_prefix = False
        for banned in banned_prefixes:
            prefix = banned['prefix'] 
            if prefix in bestMatch.lower():
                banned_prefix = True
                break

        if banned_prefix:
            continue

        print("Best Match", bestMatch)

        driver.execute_script(f'this.game.currentGame.userSubmit("{bestMatch}","{bestMatch}")')
        time.sleep(1.2)

        New_TARGET = driver.execute_script("return this.game.currentGame.targetLines")
        if TARGET != New_TARGET:
            break


driver.close()