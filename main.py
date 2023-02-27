from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import threading
import sys
import pandas as pd


#MUST BE THE EXACT SAME CHARACTERS FOR WINNING OPTION AND CANDIDATES
__candidates = {"Option 1": 0, "Option 2": 0}
__winningOption = "Option 1"
__question = "Question here" #The question asked on the google form
__SHEET_LINK = "https://docs.google.com/spreadsheets/d/1bHa6qSbfpBf4nXgOdp7hU3zM2vXKMZb61nlV9vu_glk/edit?usp=sharing"
__cheatForm = "https://forms.gle/VtidC5MaGuSuc3hx8"


def setVariables():



def __submitResponse(option):
    global cheatForm

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    driver.get(cheatForm)
    time.sleep(0.1)
    driver.find_element(by=By.XPATH, value=f"//*[contains(@data-value,'{option}')]").click()
    time.sleep(0.05)

    button2 = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div/span/span[text()="Submit"]')))
    button2.click()
    driver.stop_client()
    driver.close()


totalVotes = 0
currentCount = 0
def __checkVote(choice):
    global candidates
    global totalVotes
    global currentCount

    if (totalVotes > 10) and float((candidates[winningOption]) / (totalVotes + 1)) < 0.51 and currentCount < 2:
        choice = winningOption
        currentCount = currentCount + 1
    else:
        currentCount = 0
    totalVotes = totalVotes + 1
    candidates[choice] = candidates[choice] + 1
    thread = threading.Thread(target=submitResponse(choice))
    thread.start()


def startVoting():
    global SHEET_LINK
    global question

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(SHEET_LINK)
    SHEET_LINK = driver.current_url
    driver.stop_client()
    driver.close()

    url = SHEET_LINK.replace('/edit#gid=', '/export?format=csv&gid=')
    prevRecord = pd.read_csv(url)
    while (True):
        record = pd.read_csv(url)
        if not (record.equals(prevRecord)):
            vals = (pd.concat([record, prevRecord]).drop_duplicates(keep=False))
            print(vals)
            col = vals.loc[:, question]
            for i in range(0, col.size):
                choice = (col.iloc[i])
                checkVote(choice)
            prevRecord = record
        else:
            time.sleep(0.05)
            print("same")