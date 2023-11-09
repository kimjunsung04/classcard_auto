import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
)


class SpellingLearning:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver  # webdriver

    def run(self, num_d: int, word_d: list) -> None:  # 핸들러 실행
        driver = self.driver
        da_e, da_k, _ = word_d
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div[2]/div[1]/div[3]",
        ).click()  # 스펠학습 진입 버튼
        time.sleep(1)
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/div/div/div/div[4]/a",
        ).click()  # 스펠학습 시작 버튼
        time.sleep(1)
        try:
            for i in range(1, num_d):
                cash_d = driver.find_element(
                    By.XPATH,
                    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span",
                ).text.split("\n")[0]
                try:
                    if cash_d.upper() != cash_d.lower():
                        try:
                            text = da_k[da_e.index(cash_d)]
                        except ValueError:
                            text = da_e[da_k.index(cash_d)]
                    else:
                        text = da_e[da_k.index(cash_d)]
                except ValueError:
                    text = "모름"
                    print("모르는 단어 감지됨")
                in_tag = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div[1]/div/div[2]/div[2]/div[{i}]/div[2]/div/div/div/div[2]/input",
                )
                in_tag.click()
                in_tag.send_keys(text)
                driver.find_element(
                    By.XPATH, "//*[@id='wrapper-learn']/div/div/div[3]"
                ).click()
                time.sleep(1.5)
                try:
                    driver.find_element(
                        By.XPATH, "//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                    ).click()
                except:
                    pass
                i += 1
                time.sleep(0.5)
        except NoSuchElementException:
            pass
