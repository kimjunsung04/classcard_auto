import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def word_get(driver: webdriver.Chrome, num_d: int) -> list:
    # 단어를 가져오는 함수
    da_e = [0] * num_d
    da_k = [0] * num_d
    da_kyn = [0] * num_d

    # 영어 단어 가져오기
    for i in range(1, num_d):
        da_e[i] = driver.find_element(
            By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div",
        ).text  # 영어단어

    # 한글 단어로 변경
    driver.find_element(
        By.CSS_SELECTOR,
        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a",
    ).click()

    # 한글 단어 가져오기
    for i in range(1, num_d):
        ko_d = driver.find_element(
            By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div",
        ).text.split("\n")  # 한글단어를 뜻과 예문으로 나눔

        da_k[i] = ko_d[0]  # 뜻만 저장
        da_kyn[i] = f"{ko_d[0]} {ko_d[1]}" if len(ko_d) != 1 else ko_d[0]  # 뜻과 예문 저장

    return [da_e, da_k, da_kyn]  # 영어단어, 한글단어, 뜻과 예문 반환


def chd_wh() -> int:
    # 학습유형 선택 함수
    os.system("cls")
    choice_dict = {
        1: "암기학습(매크로) 지원하지 않음",
        2: "리콜학습(매크로)",
        3: "스펠학습(매크로)",
        4: "테스트학습(매크로) 지원하지 않음",
        5: "암기학습(API 요청[경고])",
        6: "리콜학습(API 요청[경고])",
        7: "스펠학습(API 요청[경고])",
    }
    print("학습유형을 선택해주세요.\nCtrl + C 를 눌러 종료")
    for key, value in choice_dict.items():
        print(f"[{key}] {value}")

    while True:
        try:
            ch_d = int(input(">>> "))
            if 1 <= ch_d <= 7:
                break
            else:
                raise ValueError
        except ValueError:
            print("학습유형을 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()

    os.system("cls")
    print(f"{ch_d}번 {choice_dict[ch_d]}를 선택하셨습니다.")
    return ch_d


def choice_set(sets: dict) -> int:
    # 학습할 세트를 선택하는 함수
    os.system("cls")
    print("학습할 세트를 선택해주세요.\nCtrl + C 를 눌러 종료")

    for set_item in sets:
        print(f"[{set_item + 1}] {sets[set_item].get('title')} | {sets[set_item].get('card_num')}")

    while True:
        try:
            ch_s = int(input(">>> "))
            if 1 <= ch_s <= len(sets):
                break
            else:
                raise ValueError
        except ValueError:
            print("세트를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()

    os.system("cls")
    print(f"{sets[ch_s - 1].get('title')}를 선택하셨습니다.")
    return ch_s - 1


def choice_class(class_dict: dict) -> int:
    # 학습할 반을 선택하는 함수
    os.system('cls' if os.name == 'nt' else 'clear')
    print("학습할 클래스를 선택해주세요.\nCtrl + C 를 눌러 종료")

    for class_item in class_dict:
        print(f"[{class_item + 1}] {class_dict[class_item].get('class_name')}")

    while True:
        try:
            ch_c = int(input(">>> "))
            if 1 <= ch_c <= len(class_dict):
                break
            else:
                raise ValueError
        except ValueError:
            print("클래스를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()

    os.system("cls")
    print(f"{class_dict[ch_c - 1].get('class_name')}를 선택하셨습니다.")
    return ch_c - 1


def check_id(id: str, pw: str) -> bool:
    # 계정 정보를 확인하는 함수
    print("계정 정보를 확인하고 있습니다. 잠시만 기다려주세요!")

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    res = requests.post("https://www.classcard.net/LoginProc", headers=headers, data=data)
    status = res.json()
    return status["result"] == "ok"


def save_id() -> dict:
    # 아이디와 비밀번호를 저장하는 함수
    while True:
        id = input("아이디를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")

        if check_id(id, password):
            data = {"id": id, "pw": password}
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("아이디 비밀번호가 저장되었습니다.\n")
            return data
        else:
            print("아이디 또는 비밀번호가 잘못되었습니다.\n")


def classcard_api_post(user_id: int, set_id: int, class_id: int, view_cnt: int, activity: int) -> None:
    # Classcard API에 데이터를 POST하는 함수
    url = "https://www.classcard.net/ViewSetAsync/resetAllLog"
    payload = f"set_idx={set_id}&activity={activity}&user_idx={user_id}&view_cnt={view_cnt}&class_idx={class_id}"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    requests.post(url, data=payload, headers=headers)


def get_account() -> dict:
    # 저장된 계정을 불러오는 함수
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data
    except Exception:
        return save_id()
