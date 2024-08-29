# 포크
본 리포지토리는 김준성님꼐서 제작하신 classcard_auto를 업데이트된 classcard에서 동작하도록 포크하여 제작하였습니다.

# 수정사항
### main.py 

* Classcard에서 세롭게 업데이트한것에 동작할수 있도록 수정
  
* 세롭게 업데이트된 Selenium에서 동작할수 있도록 수정

* 필요없는 webdriver.autoinstaller 삭제 (Selenium에서 없어도 실행가능함.)

# 주의 사항
본 풀리퀘스트는 완성되지 않았습니다. 단순히 main.py와 여러 라이브러리들만 수정하였습니다.

동작하지 않은 기능들은 다음과 같습니다.

* 암기학습

* 테스트

혹시 몰라 rote_learning.py와 test_learning.py는 남겨놓겠지만 사용하지 않습니다.
  
# 클래스카드 오토 매크로

> [!Warning]
> 학습 목적으로만 사용해주세요.<br>
> 해당 프로그램을 사용하여 발생한 모든 문제는 사용자에게 책임이 있습니다.

## 시연영상

https://github.com/kimjunsung04/classcard_auto/assets/70435510/3261a3ad-7820-4796-9cfd-48d01957f699

## Getting Started / 어떻게 시작하나요?

### Prerequisites / 선행 조건

아래 사항들이 설치가 되어있어야합니다.

```
Chrome
```

### Installing / 설치

아래 사항들로 현 프로젝트에 관한 모듈들을 설치할 수 있습니다.

```
pip install -r requirements.txt
```

### 구현방법

```
셀레니움을 이용하여 자동화를 하였습니다.
리콜, 스펠, 테스트 학습 이전에 단어표를 먼저 학습하고
맞는 단어끼리 매칭하여 정답을 맞추는 방식으로 구현하였습니다.
```

## Issues / 이슈

동작에 문제가 있다면 사용환경, 오류코드를 꼭 남겨주세요.

## Contribution / 기여

소스 수정사항이 있다면 Pull requests 로 열어주세요.

## License / 라이센스

이 프로젝트는 MIT License 라이센스가 부여되어 있습니다.
