from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
from selenium.webdriver.common.keys import Keys


def run_model():
    # Open web driver and go to webpage
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://research.google.com/semantris/")

    # At this moment user must manually press play button
    # TODO : Find the way how to press the button automatically

    # Needs for game to be loaded
    time.sleep(15)

    wordlist = []
    words = []
    index = 0

    target_index = 0

    while True:

        # Word/Words for which we need to find similar words
        TARGET = []

        # Sometimes target lines take time to load so we wait until its loaded
        while len(TARGET) == 0:
            TARGET = driver.execute_script(
                "return this.game.currentGame.targetLines")

        # Target Reset condition
        if target_index > 0 and len(TARGET) >= target_index and index >= len(words):
            target_index = 0

        print("target", TARGET)
        # If the target is multiple word (like book name) we need to modify it so we can use API call
        TARGET = TARGET[target_index].replace(' ', '+')

        # Saving all targets
        wordlist.append(TARGET)

        # Comparing if our submitted word worked correctly. If not so we increase index so we can take
        # Next word from the list of similar words for current target
        if len(wordlist) > 1 and wordlist[-1] == wordlist[-2]:
            index += 1
        else:
            words = requests.get(
                f'http://api.datamuse.com/words?ml={TARGET}').json()
            index = 0

        # Out of bound so we move to next word
        if len(words) <= index:
            target_index += 1
            continue

        bestMatch = words[index]['word']
        print("Best Match", bestMatch)

        # Manually check if the target and best match have some common prefixes
        # As it violates game rules
        if bestMatch[:3].lower() in TARGET.lower():
            index += 1
            continue

        # We input our best match
        driver.execute_script(
            f'this.game.currentGame.userSubmit("{bestMatch}","{bestMatch}")')

        # Sleep for some time
        time.sleep(2 - len(wordlist) * 0.01 if 2 >=
                   len(wordlist) * 0.01 else 0.2)

        # Once game is over we print the score
        # BOARD: 4, ENDED: 3, PLAYING: 2, READY: 1

        game_state = driver.execute_script(
            "return this.game.currentGame.state")

        if game_state == "3":
            print("Score:", driver.execute_script(
                "return this.game.currentGame.points"))
            break

    driver.close()
