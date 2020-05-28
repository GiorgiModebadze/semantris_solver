from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome("./chromedriver")
driver.get("https://research.google.com/semantris/")

#TODO : Find the way how to press the button automatically 
time.sleep(15)

for i in range (10):

    TARGET =  driver.execute_script("return this.game.currentGame.targetLines")
    print(TARGET[0])
    
    #TODO : Find the best way for finding best matching word. 

    bestMatch = "person"
    driver.execute_script(f'this.game.currentGame.userSubmit("{bestMatch}","{bestMatch}")')

    time.sleep(2)

time.sleep(10000)
driver.close()