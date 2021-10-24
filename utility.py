import re
from selenium import webdriver

def word_get(driver, num_d):
    da_e=[0 for i in range(num_d)]
    da_k=[0 for i in range(num_d)]
    da_kyn=[0 for i in range(num_d)]

    for i in range(1, num_d):
        da_e[i] = driver.find_element_by_xpath(f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div").text

    driver.find_element_by_css_selector(
                        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a"
                    ).click()

    for i in range(1, num_d):
        ko_d = driver.find_element_by_xpath(f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div").text
        ko_d = ko_d.split("\n")

        try:
            if bool(re.search(r'[a-z]', ko_d[1])):
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
[0] 끝내기
[1] 암기학습
[2] 리콜학습
[3] 스펠학습
[4] 테스트학습
    """
    )
    while 1:
        try:
            ch_d = int(input(">>> "))
        except:
            print("학습유형은 정수로만 선택 가능합니다. 다시 입력해주세요.")
        else:
            for i in range(0, 5):
                if i == ch_d:
                    ch = True
                    break
                ch = False
            if ch == True:
                break

            print("학습유형을 다시 입력해주세요.")
    return ch_d