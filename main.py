import time
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from handler.recall_learning import RecallLearning
from handler.spelling_learning import SpellingLearning
from selenium.webdriver.chrome.options import Options

# 함수 불러오기
from utility import (
    chd_wh,
    get_account,
    word_get,
    choice_set,
    choice_class,
    classcard_api_post,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

# 계정 정보 가져오기
account = get_account()
print("크롬 드라이브를 불러오고 있습니다. 잠시만 기다려주세요!")

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--log-level=1')

# 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)

# 로그인 시행
driver.get("https://www.classcard.net/Login")
id_element = driver.find_element(By.ID, "login_id")
pw_element = driver.find_element(By.ID, "login_pwd")

# Autofill 억제
id_element.clear()
id_element.send_keys(account["id"])  # 아이디 입력
pw_element.send_keys(account["pw"])  # 비밀번호 입력
driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div/div/div/form/div[3]/a",
).click()  # 로그인 버튼 클릭

time.sleep(1)  # 로딩 대기

# 클래스 선택
class_dict = {}
class_list_element = driver.find_element(
    By.CSS_SELECTOR,
    "body > div.mw-1080 > div:nth-child(6) > div > div > div.left-menu > div.left-item-group.p-t-none.p-r-lg > div.m-t-sm.left-class-list",
)

# 클래스 목록 가져오기
class_count = len(class_list_element.find_elements(By.TAG_NAME, "a"))
for class_item, i in zip(
        class_list_element.find_elements(By.TAG_NAME, "a"),
        range(class_count),
):
    class_temp = {}
    class_temp["class_name"] = class_item.text
    class_temp["class_id"] = class_item.get_attribute("href").split("/")[-1]

    if class_temp["class_id"] == "joinClass":
        break
    class_dict[i] = class_temp

# 클래스가 없는 경우 처리
if len(class_dict) == 0:
    print("클래스가 없습니다.")
    quit()
elif len(class_dict) == 1:
    choice_class_val = 0  # 자동으로 첫 번째 클래스 선택
else:
    choice_class_val = choice_class(class_dict=class_dict)  # 클래스 선택

# 선택한 클래스 ID 가져오기
class_id = class_dict[choice_class_val].get("class_id")
driver.get(f"https://www.classcard.net/ClassMain/{class_id}")  # 클래스 페이지로 이동
time.sleep(1)  # 로딩 대기

# 세트 선택
sets_div = driver.find_element(
    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div"
)
sets = sets_div.find_elements(By.CLASS_NAME, "set-items")
sets_count = len(sets)
sets_dict = {}

# 세트 목록 가져오기
for set_item, i in zip(sets, range(sets_count)):
    set_temp = {}
    set_temp["card_num"] = (
        set_item.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "span").text
    )  # 카드 개수 가져오기
    set_temp["title"] = set_item.find_element(By.TAG_NAME, "a").text.replace(
        set_temp["card_num"], ""
    )  # 카드 개수 제거
    set_temp["set_id"] = set_item.find_element(By.TAG_NAME, "a").get_attribute(
        "data-idx"
    )  # 세트 아이디 가져오기
    sets_dict[i] = set_temp

# 세트 선택
set_choice = choice_set(sets_dict)
set_site = (f"https://www.classcard.net/set/{sets_dict[set_choice]['set_id']}/{class_id}")
driver.get(set_site)  # 세트 페이지로 이동
time.sleep(1)  # 로딩 대기

# 유저 ID 가져오기
user_id = int(driver.execute_script("return c_u;"))

# 단어 저장
driver.find_element(
    By.CSS_SELECTOR,
    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md.pos-relative > div.dropdown > a",
).click()  # 학습구간 선택
driver.find_element(
    By.CSS_SELECTOR,
    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md.pos-relative > div.dropdown.open > ul > li:nth-child(1) > a",
).click()  # 학습구간 전체로 변경

# 페이지 소스를 HTML로 파싱
html = BeautifulSoup(driver.page_source, "html.parser")
cards_ele = html.find("div", class_="flip-body")  # 카드들을 찾음
num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1  # 카드의 개수를 구함
time.sleep(0.5)  # 로딩 대기

# 단어 가져오기
word_d = word_get(driver, num_d)
da_e, da_k, da_kyn = word_d

# 학습 유형 선택 및 실행
while True:
    ch_d = chd_wh()  # 학습유형 입력

    if ch_d == 1:
        print("암기학습을 시작합니다.")
        controler = RoteLearning(driver=driver)  # 암기 학습 클래스 생성
        controler.run(num_d=num_d)  # 학습 시작
    elif ch_d == 2:
        print("리콜학습을 시작합니다.")
        controler = RecallLearning(driver=driver)  # 암기 학습 클래스 생성
        controler.run(num_d=num_d, word_d=word_d)  # 학습 시작
    elif ch_d == 3:
        print("스펠학습을 시작합니다.")
        controler = SpellingLearning(driver=driver)  # 스펠 학습 클래스 생성
        controler.run(num_d=num_d, word_d=word_d)  # 학습 시작
    elif ch_d == 4:
        print("테스트학습은 지원하지 않습니다.")
        break
    elif ch_d == 5:
        print("암기학습 API 요청을 시작합니다.")
        classcard_api_post(
            user_id=user_id,
            set_id=sets_dict[set_choice]["set_id"],
            class_id=class_id,
            view_cnt=num_d,
            activity=1,
        )
    elif ch_d == 6:
        print("리콜학습 API 요청을 시작합니다.")
        classcard_api_post(
            user_id=user_id,
            set_id=sets_dict[set_choice]["set_id"],
            class_id=class_id,
            view_cnt=num_d,
            activity=2,
        )
    elif ch_d == 7:
        print("스펠학습 API 요청을 시작합니다.")
        classcard_api_post(
            user_id=user_id,
            set_id=sets_dict[set_choice]["set_id"],
            class_id=class_id,
            view_cnt=num_d,
            activity=3,
        )

    print("학습이 종료되었습니다.")
    driver.get(set_site)  # 다시 세트 페이지로 이동
    time.sleep(1)
