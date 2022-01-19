# NotePad — Penguin's 메모장
The NotePad application implemented in Python using PyQt5. The Ui was designed in Qt Designer.
UI and features cloned Windows Notepad.

<a href="https://www.python.org">
<img src="https://img.shields.io/badge/Python3+-3776AB?style=flat&logo=PYTHON&logoColor=white&link=https://www.python.org/"></a>
<a href="https://www.anaconda.com">
<img src="https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=Anaconda&logoColor=white&link=https://www.anaconda.com/"></a>
<a href="https://qt-brandbook.webflow.io">
<img src="https://img.shields.io/badge/Qt-41CD52?style=flat&logo=Qt&logoColor=white&link=https://qt-brandbook.webflow.io/"></a>

## UI
![notepad-3](https://user-images.githubusercontent.com/69224744/149991487-602cc4a0-16a7-42be-aaa2-0d7bf65658ee.gif)


## Windows based:
### Prerequisite
- PyQt5
- Qt Designer (Only for developers for editing layouts)

## Feature
- 오픈된 파일의 파일명을 제목표시줄에 표시
- 작성 내용에 변화가 감지되면 제목 표시줄에 반영되도록 구현. 변경 사항이 없을 경우, * 제거
  ![notepad-4](https://user-images.githubusercontent.com/69224744/149991499-834cd048-4f40-43c0-a248-ecc15363f557.gif)
- 단어 검색 기능
  - 대/소문자 구분과 검색 방향 선택이 가능하도록 구현
  ![notepad-5](https://user-images.githubusercontent.com/69224744/150146594-4ceaeeb9-9ef8-4dfb-9bb8-09f823824b32.gif)
- 시간/날짜 삽입 기능. 년-월-일 시간 형태로 삽입
  - ex) 2022-01-19 10:39:35
- 메모장 정보에 GitHub 연동


## 개선 사항
- 상황에 따라 일부 버튼 비활성화 상태 변경이 필요
