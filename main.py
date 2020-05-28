from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("./chromedriver")
driver.get("https://research.google.com/semantris/")

#TODO : Find the way how to press the button automatically 
time.sleep(15)

wordlist = []
words = []
index = 0

target_index = 0

while True:

    TARGET = []
    while len(TARGET) == 0:  
        TARGET =  driver.execute_script("return this.game.currentGame.targetLines")

    if target_index > 0 and len(TARGET) >= target_index and index>=len(words):
        target_index = 0

    print("target", TARGET)
    TARGET = TARGET[target_index].replace(' ', '+')
    
    wordlist.append(TARGET)


    if len(wordlist) > 1 and wordlist[-1] == wordlist[-2]:
        index += 1
    else:
        words = requests.get(f'http://api.datamuse.com/words?ml={TARGET}').json()
        index = 0

    # out of bound so we move to next word
    if len(words) <= index:
        target_index+=1
        continue
    

    bestMatch = words[index]['word']
    print("Best Match", bestMatch)

    if bestMatch[:3].lower() in TARGET.lower():
        print("We Continues")
        index +=1
        continue

    driver.execute_script(f'this.game.currentGame.userSubmit("{bestMatch}","{bestMatch}")')
    time.sleep(2 - len(wordlist) * 0.01 if 2 >= len(wordlist) * 0.01 else 0.2 )


driver.close()