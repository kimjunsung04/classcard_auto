import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class RoteLearning:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver  # webdriver

    def run(self, num_d: int) -> None:  # 핸들러 실행
        driver = self.driver
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div[2]/div[1]/div[1]",
        ).click()
        time.sleep(1)
        driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/div/div/div/div[4]/a",
        ).click()
        for _ in range(1, num_d):
            time.sleep(2)
            try:
                self.button_auto_pass(
                    driver,
                    "#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box",  # 의미 보기
                    0.5,
                    "#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box",  # 이제 알아요
                )  # 카드 넘기기
            except Exception:
                break
        time.sleep(0.5)
        driver.find_element(
            By.CSS_SELECTOR,
            "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a",
        ).click()

    def button_auto_pass(
        self, driver, btn1: str, time_sec: int, btn2: str
    ) -> None:  # 버튼 자동 클릭
        driver.find_element(By.CSS_SELECTOR, btn1).click()  # 1번 버튼 클릭
        time.sleep(time_sec)
        driver.find_element(By.CSS_SELECTOR, btn2).click()  # 2번 버튼 클릭
