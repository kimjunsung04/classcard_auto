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
        da_e, _, da_kyn = word_d
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div[2]/div[1]/div[2]",
        ).click()  # 리콜학습 진입 버튼
        time.sleep(1)
        driver.find_element(
            By.CSS_SELECTOR,
            "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
        ).click()  # 리콜학습 시작 버튼
        time.sleep(1)
        for i in range(num_d):  # 단어 수 만큼 반복
            try:
                cash_d = driver.find_element(
                    By.XPATH,
                    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i+1}]/div[1]/div/div/div/div[1]",
                ).text  # 메인 단어 추출

                cash_dby = [  # 선택창에서 모름 제외 3개 단어 추출
                    driver.find_element(
                        By.XPATH,
                        f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i+1}]/div[3]/div[{j+1}]/div[2]",
                    ).text
                    for j in range(3)
                ]

                ck = False  # 찾을수없는 단어 감지
                if cash_d.upper() != cash_d.lower():  # 단어가 영어일때
                    with contextlib.suppress(Exception):
                        for j in range(3):  # 3개의 선택지중
                            # 단어가 같은것이 있으면
                            if da_e.index(cash_d) == da_kyn.index(cash_dby[j]):
                                driver.find_element(  # 클릭
                                    By.XPATH,
                                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i+1}]/div[3]/div[{j+1}]/div[2]",
                                ).click()
                                ck = True  # 찾음
                                break
                    if ck != True:  # 못찾았으면
                        print("\n찾을수없는 단어 감지로 랜덤으로 찍기발동!!\n")  # 랜덤으로 찍기
                        driver.find_element(  # 랜덤으로 클릭
                            By.XPATH,
                            f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i+1}]/div[3]/div[{random.randint(1, 3)}]/div[2]",
                        ).click()
                        time.sleep(2)
                        with contextlib.suppress(Exception):  # 예외 발생시 (긴급탈출)
                            driver.find_element(
                                By.XPATH,
                                "//*[@id='wrapper-learn']/div/div/div[3]/div[2]",
                            ).click()
                time.sleep(2)  # 2초 대기
            except Exception:  # 예외 발생시 (긴급탈출)
                driver.find_element(
                    By.XPATH, "/html/body/div[1]/div/div[1]/div[1]"
                ).click()  # 학습 종료 버튼 클릭
                time.sleep(1)
                driver.find_element(
                    By.XPATH, "//*[@id='wrapper-learn']/div[2]/div/div/div/div[5]/a[3]"
                ).click()  # 학습 종료 확인 버튼 클릭
                break
