from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_driver():
    DRIVER_PATH = 'D:/Documents/Code/python/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    return driver

def get_deck_links(driver):
    links = []
    driver.get('https://gre.magoosh.com/flashcards/vocabulary/decks')
    decks = driver.find_elements(By.CLASS_NAME,"flashcard-card")
    for deck in decks:
        deck_title = deck.find_element(By.CLASS_NAME,"card-title").text
        if deck_title not in ['Magoosh GRE']:
            links.append((deck_title, deck.find_elements(By.TAG_NAME,"a")[0].get_attribute('href')))
    return links

def get_words_and_meanings(deck, link, driver):
    words_list = {'deck': [], 'word':[], 'meaning':[], 'example':[]}
    driver.get(link)
    for _ in range(54):
        # click to see the meaning
        click_for_meaning = driver.find_element(By.CLASS_NAME,"card-footer")
        driver.execute_script("arguments[0].scrollIntoView();", click_for_meaning)
        driver.execute_script("arguments[0].click();", click_for_meaning)
        time.sleep(2)
        try:
            word = driver.find_element(By.CLASS_NAME,"flashcard-word").text
            if word not in words_list['word']:
                words_list['example'].append(driver.find_element(By.CLASS_NAME,"flashcard-example").text)
                words_list['meaning'].append(driver.find_element(By.CLASS_NAME,"flashcard-text").text)
                words_list['word'].append(word)
                words_list['deck'].append(deck)
        except:
            pass
        # I knew the word
        next_word = driver.find_element(By.CLASS_NAME,"card-footer-success")
        driver.execute_script("arguments[0].scrollIntoView();", next_word)
        driver.execute_script("arguments[0].click();", next_word)

        time.sleep(2)
    return pd.DataFrame(words_list)

def run_scraper():
    driver = get_driver()
    deck_links = get_deck_links(driver)
    final_words_list = pd.DataFrame({'deck': [], 'word':[], 'meaning':[], 'example':[]})
    for deck, link in deck_links:
        words_list = get_words_and_meanings(deck, link, driver)
        final_words_list = pd.concat([final_words_list, words_list], axis = 0)
        words_list.to_csv("{0}.csv".format(deck), index = False)
        time.sleep(5)
    driver.quit()
    final_words_list.to_csv("magoosh_word_list.csv", index = False)
    return

if __name__ == '__main__':
    run_scraper()