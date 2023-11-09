import contextlib
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class RecallLearning:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver  # webdriver

    def run(self, num_d: int, word_d: list) -> None:  # 핸들러 실행
        driver = self.driver
        da_e, da_k, _ = word_d
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div[2]/div[1]/div[2]",
        ).click()  # 리콜학습 진입 버튼
        time.sleep(1)
        driver.find_element(
            By.CSS_SELECTOR,
            "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
        ).click()  # 리콜학습 시작 버튼
        time.sleep(2)
        for i in range(num_d):  # 단어 수 만큼 반복
            try:
                cash_d = driver.find_element(
                    By.XPATH,
                    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i+1}]/div[1]/div/div/div/div[1]/span",
                ).text  # 메인 단어 추출

                choice_list_element = driver.find_element(
                    By.XPATH,
                    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i+1}]/div[3]",
                )
                for choice_item in choice_list_element.find_elements(
                    By.TAG_NAME, "div"
                ):
                    choice_text = choice_item.text
                    if choice_text in da_k:
                        if cash_d == da_e[da_k.index(choice_text)]:
                            choice_item.click()
                            break
                    elif choice_text in da_e:
                        if cash_d == da_k[da_e.index(choice_text)]:
                            choice_item.click()
                            break
                    else:
                        continue
                else:
                    print("모르는 단어 감지됨")
                    choice_list_element.find_elements(By.TAG_NAME, "div")[
                        random.randint(0, 3)
                    ].click()
                time.sleep(3)
            except Exception as e:  # 예외 발생 시 학습 종료
                driver.find_element(
                    By.XPATH, "/html/body/div[1]/div/div[1]/div[1]"
                ).click()  # 학습 종료 버튼 클릭
                time.sleep(1)
                driver.find_element(
                    By.XPATH, "//*[@id='wrapper-learn']/div[2]/div/div/div/div[5]/a[3]"
                ).click()  # 학습 종료 확인 버튼 클릭
                break
