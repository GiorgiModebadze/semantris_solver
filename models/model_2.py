from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
from selenium.webdriver.common.keys import Keys
from operator import itemgetter

'''
    First Model provided respectable score of avg 13000, but it can clearly be improved with better model.
    Once the game is loaded it loads start file, which containes all the possible words. We can utilize it
    For our model generation
'''


def run_model(model_name):

    # Loading custom model that we generated
    with open(f'{model_name}.json', 'rb') as fout:
        data = json.load(fout)

    res = {}

    for i in data:
        res.update(i)

    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://research.google.com/semantris/")

    time.sleep(15)

    wordlist = []
    words = []
    index = 0

    target_index = 0

    while True:

        TARGET = []

        # Sometimes target lines take time to load so we wait until its loaded
        while len(TARGET) == 0:
            TARGET = driver.execute_script(
                "return this.game.currentGame.targetLines")

        print("target", TARGET)

        # As target can have many words in it we can utilize it to get best match for all of them
        # Not only for one of them

        full = []
        for i in TARGET:
            full += res[i]

        # Sort best matches
        words = sorted(full, key=itemgetter('score'), reverse=True)

        for word in words:

            bestMatch = word['word']

            # Games allows for each target to give banned prefix. This allows more precise control of the
            # Words which can not be submitted

            banned_prefixes = driver.execute_script(
                "return this.game.currentGame.bannedPrefixes")
            banned_prefix = False

            for banned in banned_prefixes:
                prefix = banned['prefix']
                if prefix in bestMatch.lower():
                    banned_prefix = True
                    break

            if banned_prefix:
                continue

            print("Best Match", bestMatch)

            driver.execute_script(
                f'this.game.currentGame.userSubmit("{bestMatch}","{bestMatch}")')
            time.sleep(1.2)

            New_TARGET = driver.execute_script(
                "return this.game.currentGame.targetLines")
            if TARGET != New_TARGET:
                break

        # Once game is over we print the score
        # BOARD: 4, ENDED: 3, PLAYING: 2, READY: 1

        game_state = driver.execute_script(
            "return this.game.currentGame.state")

        if game_state == "3":
            print("Score:", driver.execute_script(
                "return this.game.currentGame.points"))
            break

    driver.close()
