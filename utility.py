import json
import re

import requests


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
