from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, json, random, getpass

# 함수불러오기
from utility import word_get
from utility import chd_wh

with open("./config.json", "r") as f:
    json_data = json.load(f)

id_d = json_data["login"]["id"]
pw_d = json_data["login"]["pw"]

if id_d == "" or pw_d == "":
    json_data["login"]["id"] = input("아이디를 입력하세요 : ")
    json_data["login"]["pw"] = getpass.getpass("비밀번호를 입력하세요 : ")
    with open("./config.json", "w") as f:
        json.dump(json_data, f, indent=4)
    print("\n아디이 비밀번호가 저장되었습니다.\n")

class_site = input("학습할 세트URL을 입력하세요 : ")

ch_d = chd_wh()

#장치 동작하지않음 방지
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
driver.get("https://www.classcard.net/Login")
time.sleep(1.5)
tag_id = driver.find_element_by_id("login_id")
tag_pw = driver.find_element_by_id("login_pwd")
tag_id.clear()

tag_id.send_keys(id_d)
tag_pw.send_keys(pw_d)

time.sleep(1)

driver.find_element_by_css_selector(
    "#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > button"
).click()

time.sleep(1)
try:
    driver.get(class_site)
except:
    print("\n입력한 URL이 잘못되어 프로그램을 종료합니다\n")
    input("종료하려면 아무 키나 누르세요...")
    quit()
time.sleep(1)

try:
    driver.find_element_by_css_selector(
        "body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
    ).click()
    driver.find_element_by_css_selector(
        "body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
    ).click()
except:
    print("\n아이디 비밀번호 불일치로 프로그램을 종료합니다.\n아이디 비밀번호를 신규 등록해주세요.\n")
    json_data["login"]["id"] = ""
    json_data["login"]["pw"] = ""
    with open("./config.json", "w") as f:
        json.dump(json_data, f, indent=4)
    input("종료하려면 아무 키나 누르세요...")
    quit()

cash_d = driver.find_element_by_xpath(
    f"/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]"
).text
num_d = [int(s) for s in cash_d.split() if s.isdigit()]
num_d = int(num_d[0] + 1)


time.sleep(0.5)

word_d = word_get(driver, num_d)

da_e = word_d[0]
da_k = word_d[1]
da_kyn = word_d[2]
while 1:
    if ch_d == 0:
        input("종료하려면 아무 키나 누르세요...")
        quit()
    elif ch_d == 1:
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

                cash_dby = [0,0,0]

                for j in range(0,3):
                    cash_dby[j] = driver.find_element_by_xpath(
                        f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j+1}]/div[2]/div"
                    ).text

                ck = False
                if cash_d.upper() != cash_d.lower():
                    try:
                        for j in range(0,3):
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
            
            element = driver.find_element_by_xpath(f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[1]/div[2]")
            driver.execute_script("arguments[0].click();", element)

            cash_dby = [0,0,0,0]

            for j in range(0,4):
                cash_dby[j] = driver.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div"
                ).text

            time.sleep(2)
            ck = False
            if cash_d.upper() != cash_d.lower():
                for j in range(0,4):
                    if da_e.index(cash_d) == da_k.index(cash_dby[j]):
                        element = driver.find_element_by_xpath(f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div")
                        driver.execute_script("arguments[0].click();", element)
                        ck = True
                        break
            else:
                for j in range(0,4):
                    if da_k.index(cash_d) == da_e.index(cash_dby[j]):
                        element = driver.find_element_by_xpath(f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div")
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


    driver.get(class_site)
    ch_d = chd_wh()
