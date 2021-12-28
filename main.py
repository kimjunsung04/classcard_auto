import random
import time
import warnings
import json
import re

import requests

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# 함수불러오기
def word_get(driver, num_d):
    da_e = [0 for i in range(num_d)]
    da_k = [0 for i in range(num_d)]
    da_kyn = [0 for i in range(num_d)]

    for i in range(1, num_d):
        da_e[i] = driver.find_element_by_xpath(
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div"
        ).text

    driver.find_element_by_css_selector(
        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a"
    ).click()

    for i in range(1, num_d):
        ko_d = driver.find_element_by_xpath(
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div"
        ).text
        ko_d = ko_d.split("\n")

        try:
            if bool(re.search(r"[a-z]", ko_d[1])):
                da_k[i] = f"{ko_d[0]}"
                da_kyn[i] = f"{ko_d[0]}"
            else:
                da_k[i] = f"{ko_d[0]}\n{ko_d[1]}"
                da_kyn[i] = f"{ko_d[0]} {ko_d[1]}"
        except:
            da_k[i] = f"{ko_d[0]}"
            da_kyn[i] = f"{ko_d[0]}"

    return [da_e, da_k, da_kyn]


def chd_wh():
    print(
        """
학습유형을 선택해주세요.
Ctrl + C 를 눌러 종료
[1] 암기학습
[2] 리콜학습
[3] 스펠학습
[4] 테스트학습
[5] 매칭
    """
    )
    while 1:
        try:
            ch_d = int(input(">>> "))
            if ch_d >= 1 and ch_d <= 5:
                break
            else:
                raise ValueError
        except ValueError:
            print("학습유형을 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()
    return ch_d


def check_id(id, pw):
    print("계정 정보를 확인하고 있습니다 잠시만 기다려주세요!")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    res = requests.post(
        "https://www.classcard.net/LoginProc", headers=headers, data=data
    )
    status = res.json()
    if status["result"] == "ok":
        return True
    else:
        return False


def save_id():
    while True:
        id = input("아이디를 입력하세요 : ")
        password = input("비밀번호를 입력하세요 : ")
        if check_id(id, password):
            data = {"id": id, "pw": password}
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("아이디 비밀번호가 저장되었습니다.\n")
            return data
        else:
            print("아이디 또는 비밀번호가 잘못되었습니다.\n")
            continue


def get_id():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            json_data["id"]
            json_data["pw"]
            return json_data
    except:
        return save_id()


warnings.filterwarnings("ignore", category=DeprecationWarning)

account = get_id()

class_site = input("학습할 세트URL을 입력하세요 : ")

ch_d = chd_wh()

print("크롬 드라이브를 불러오고 있습니다 잠시만 기다려주세요!")

# 장치 동작하지않음 방지
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    service=Service(chromedriver_autoinstaller.install()), options=options
)

driver.get("https://www.classcard.net/Login")
tag_id = driver.find_element_by_id("login_id")
tag_pw = driver.find_element_by_id("login_pwd")
tag_id.clear()
tag_id.send_keys(account["id"])
tag_pw.send_keys(account["pw"])
driver.find_element_by_css_selector(
    "#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > button"
).click()

try:
    time.sleep(1)
    driver.get(class_site)
    driver.find_elements(By.XPATH, "//div[@class='p-b-sm']")
except:
    print("\n입력한 URL이 잘못되어 프로그램을 종료합니다\n")
    input("종료하려면 아무 키나 누르세요...")
    quit()
time.sleep(1)

driver.find_element_by_css_selector(
    "body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
).click()
driver.find_element_by_css_selector(
    "body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
).click()

html = BeautifulSoup(driver.page_source, "html.parser")
cards_ele = html.find("div", class_="flip-body")
num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1

time.sleep(0.5)

word_d = word_get(driver, num_d)

da_e = word_d[0]
da_k = word_d[1]
da_kyn = word_d[2]
while 1:
    if ch_d == 1:
        driver.find_element_by_css_selector(
            "#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(1)"
        ).click()
        for i in range(1, num_d):
            time.sleep(2.5)
            try:
                driver.find_element_by_css_selector(
                    "#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box"
                ).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(
                    "#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box"
                ).click()
            except:
                break
        time.sleep(1)
        driver.find_element_by_css_selector(
            "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a"
        ).click()
    elif ch_d == 2:
        driver.find_element_by_css_selector(
            "#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(2)"
        ).click()

        time.sleep(2)

        for i in range(1, num_d):
            try:
                cash_d = driver.find_element_by_xpath(
                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span"
                ).text

                cash_dby = [0, 0, 0]

                for j in range(0, 3):
                    cash_dby[j] = driver.find_element_by_xpath(
                        f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j+1}]/div[2]/div"
                    ).text

                ck = False
                if cash_d.upper() != cash_d.lower():
                    try:
                        for j in range(0, 3):
                            if da_e.index(cash_d) == da_kyn.index(cash_dby[j]):
                                driver.find_element_by_xpath(
                                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j+1}]/div[2]"
                                ).click()
                                ck = True
                                break
                    except:
                        pass
                    if ck != True:
                        print("\n찾을수없는 단어 감지로 랜덤으로 찍기발동!!\n")
                        driver.find_element_by_xpath(
                            f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{random.randint(1, 4)}]/div[2]"
                        ).click()
                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath(
                                f"//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                            ).click()
                        except:
                            pass
                time.sleep(2.5)
            except:
                driver.find_element_by_xpath(
                    f"/html/body/div[1]/div/div[1]/div[1]"
                ).click()
                time.sleep(1)
                driver.find_element_by_xpath(
                    f"//*[@id='topBackModal']/div[2]/div/div/a[5]"
                ).click()
                break
    elif ch_d == 3:
        driver.find_element_by_css_selector(
            "#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(3)"
        ).click()

        time.sleep(2)
        try:
            for i in range(1, num_d):
                cash_d = driver.find_element_by_xpath(
                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span[1]"
                ).text
                print(cash_d)
                if cash_d.upper() != cash_d.lower():
                    try:
                        text = da_k[da_e.index(cash_d)]
                    except ValueError:
                        text = da_e[da_k.index(cash_d)]
                else:
                    text = da_e[da_k.index(cash_d)]
                in_tag = driver.find_element_by_css_selector(
                    "#wrapper-learn > div > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-bottom > div > div > div > div.text-normal.spell-input > input"
                )
                in_tag.click()
                in_tag.send_keys(text)
                driver.find_element_by_xpath(
                    "//*[@id='wrapper-learn']/div/div/div[3]"
                ).click()
                time.sleep(1.5)
                try:
                    driver.find_element_by_xpath(
                        "//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                    ).click()
                except:
                    pass
                i += 1
                time.sleep(1)
        except NoSuchElementException:
            pass
    elif ch_d == 4:
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[4]/div/div/div[3]/a[1]"
        ).click()
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath(
                "/html/body/div[26]/div[2]/div/div[3]/a"
            ).click()

            driver.get(class_site)

            driver.find_element_by_xpath(
                "/html/body/div[1]/div[4]/div/div/div[3]/a[1]"
            ).click()

            time.sleep(1)
        except:
            pass

        driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div[4]/a"
        ).click()

        driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[1]/div[3]/div[3]/a"
        ).click()

        time.sleep(2)
        for i in range(1, 21):
            cash_d = driver.find_element_by_xpath(
                f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[1]/div[2]/div/div/div"
            ).text

            element = driver.find_element_by_xpath(
                f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[1]/div[2]"
            )
            driver.execute_script("arguments[0].click();", element)

            cash_dby = [0, 0, 0, 0]

            for j in range(0, 4):
                cash_dby[j] = driver.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div"
                ).text

            time.sleep(2)
            ck = False
            if cash_d.upper() != cash_d.lower():
                for j in range(0, 4):
                    if da_e.index(cash_d) == da_k.index(cash_dby[j]):
                        element = driver.find_element_by_xpath(
                            f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div"
                        )
                        driver.execute_script("arguments[0].click();", element)
                        ck = True
                        break
            else:
                for j in range(0, 4):
                    if da_k.index(cash_d) == da_e.index(cash_dby[j]):
                        element = driver.find_element_by_xpath(
                            f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div"
                        )
                        driver.execute_script("arguments[0].click();", element)
                        ck = True
                        break
            if ck != True:
                print("\n찾을수없는 단어 감지로 랜덤으로 찍기발동!!\n")
                driver.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{random.randint(1, 4)}]/label/div/div"
                ).click()
                time.sleep(2)
            time.sleep(3)
    if ch_d == 5:
        print("Ctrl + C 를 눌러 강제 종료")
        ##매칭 게임
        driver.find_element_by_css_selector(
            "a.w-120:nth-child(2) > div:nth-child(1)"
        ).click()
        time.sleep(1)

        # 단어 1000개 이상
        try:
            driver.find_element_by_xpath(
                "/html/body/div[53]/div[2]/div/div[2]/a[3]"
            ).click()
            time.sleep(1)
        except Exception as e:
            pass
        driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div/div[1]/div[4]/a[1]"
        ).click()
        # 매칭 게임 시작
        time.sleep(2.5)
        past_cards = ""
        while True:
            try:
                html = BeautifulSoup(driver.page_source, "html.parser")
                # 점수 순으로 정렬
                unsorted_cards = dict()
                cards = html.find("div", class_="match-body").get_text(strip=True)
                # 이전 카드와 같으면 다시
                if past_cards == cards:
                    raise NotImplementedError
                for i in range(4):
                    left_card = html.find("div", id="left_card_{}".format(i))
                    score = int(
                        left_card.find("span", class_="card-score").get_text(strip=True)
                    )
                    left_card.find("span", class_="card-score").decompose()
                    question = left_card.get_text(strip=True)
                    unsorted_cards["{}_{}".format(question, str(i))] = score
                    # 점수 높은 순서로 배열
                    sorted_lists = {
                        k: v
                        for k, v in sorted(
                            unsorted_cards.items(), key=lambda item: item[1]
                        )
                    }.keys()
                for k in sorted_lists:
                    word = k.split("_")[0]
                    order = k.split("_")[1]
                    # answer = list[word]
                    answer = da_k[da_e.index(word)]

                    for j in range(4):
                        right_card = html.find(
                            "div", id="right_card_{}".format(j)
                        ).get_text(strip=True)
                        if right_card == answer:
                            left_element = driver.find_element_by_id(
                                "left_card_{}".format(order)
                            )
                            right_element = driver.find_element_by_id(
                                "right_card_{}".format(j)
                            )
                            try:
                                left_element.click()
                                right_element.click()
                            except ElementClickInterceptedException:
                                action = ActionChains(driver)
                                action.click(on_element=left_element)
                                action.click(on_element=right_element)
                                action.perform()
                                action.reset_actions()
                            raise NotImplementedError
                        else:
                            continue
            except NotImplementedError:
                if driver.find_element_by_class_name("rank-info").size["height"] > 0:
                    print("완료되었습니다")
                    driver.find_element_by_css_selector(".btn-default").click()
                    time.sleep(1)
                    break
                else:
                    past_cards = cards
            except KeyboardInterrupt:
                break

    driver.get(class_site)
    ch_d = chd_wh()
